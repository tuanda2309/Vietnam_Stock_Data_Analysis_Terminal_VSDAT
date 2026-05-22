from datetime import datetime, timedelta, timezone

import numpy as np

try:
    from zoneinfo import ZoneInfo
except ImportError:  # Python < 3.9 fallback, gần như không xảy ra với project này
    ZoneInfo = None

try:
    from vnstock3 import Vnstock
except ImportError:
    from vnstock import Vnstock

from utils.dataframe_utils import prepare_ohlcv_dataframe
from utils.helpers import safe_float, round_number, round_price_vn, normalize_price_value
from utils.indicators import add_technical_indicators
from utils.support_resistance import find_support_resistance
from utils.risk import calculate_risk_management
from services.market_service import analyze_vnindex_market
from services.analysis_service import analyze_signal, build_suggested_order


# ==========================================================
# API LẤY DỮ LIỆU VÀ PHÂN TÍCH CHỨNG KHOÁN
# ==========================================================

try:
    VN_TZ = ZoneInfo("Asia/Ho_Chi_Minh") if ZoneInfo else timezone(timedelta(hours=7))
except Exception:
    # Một số máy Windows thiếu tzdata, dùng UTC+7 cố định để local vẫn chạy được.
    VN_TZ = timezone(timedelta(hours=7))


def get_previous_weekday(day):
    """Lùi về ngày làm việc gần nhất, bỏ qua Thứ 7 / Chủ nhật."""
    day = day - timedelta(days=1)
    while day.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
        day = day - timedelta(days=1)
    return day


def get_expected_vietnam_trading_session_date(now_vn):
    """
    Xác định phiên giao dịch gần nhất theo giờ Việt Nam.

    Lý do cần hàm này:
    - Render thường chạy theo UTC, còn máy local ở Việt Nam là UTC+7.
    - Sau 00:00 ở Việt Nam, phiên mới thực tế chưa mở cửa, nên phiên gần nhất vẫn là ngày giao dịch hôm trước.
    - Nếu chỉ so sánh `df.iloc[-1]['time'].date() == datetime.now().date()` thì local rất dễ hiểu nhầm
      dữ liệu ngày hôm trước là dữ liệu cũ và tính priceChange = 0.
    """
    session_day = now_vn.date()

    # Cuối tuần: phiên gần nhất là Thứ 6.
    while session_day.weekday() >= 5:
        session_day = session_day - timedelta(days=1)

    # Trước giờ mở cửa, phiên gần nhất vẫn là ngày làm việc trước đó.
    # HOSE/HNX/UPCoM mở cửa khoảng 09:00, nên dùng mốc 09:00 để tránh lỗi sau nửa đêm.
    if now_vn.weekday() < 5 and now_vn.hour < 9:
        session_day = get_previous_weekday(now_vn.date())

    return session_day


def get_stock_analysis_data(symbol):
    try:
        if not symbol or symbol.strip() == "":
            return {"error": "Mã cổ phiếu không được để trống"}, 400

        symbol_upper = symbol.strip().upper()
        stock_api = Vnstock().stock(symbol=symbol_upper, source="VCI")

        current_time = datetime.now(VN_TZ)
        start_date = (current_time - timedelta(days=365 * 2)).strftime("%Y-%m-%d")
        end_date = current_time.strftime("%Y-%m-%d")

        raw_df = stock_api.quote.history(start=start_date, end=end_date, interval="1D")
        df = prepare_ohlcv_dataframe(raw_df, multiply_price_by_1000=True)

        if df is None or df.empty:
            return {"error": f"Không tìm thấy dữ liệu giao dịch cho mã: {symbol_upper}"}, 442

        if len(df) < 20:
            return {"error": f"Dữ liệu cho mã {symbol_upper} quá ít để phân tích kỹ thuật"}, 442

        # Lấy intraday/realtime nếu có. Không crash nếu vnstock lỗi intraday.
        realtime_price = None
        has_intraday = False
        try:
            intraday = stock_api.quote.intraday()
            if intraday is not None and not intraday.empty and "price" in intraday.columns:
                realtime_price = normalize_price_value(intraday.iloc[-1]["price"], True)
                has_intraday = realtime_price is not None
        except Exception:
            pass

        last_row_date = df.iloc[-1]["time"].date()
        expected_session_date = get_expected_vietnam_trading_session_date(current_time)
        latest_history_close = safe_float(df.iloc[-1]["close"])
        pricing_mode = "unknown"

        if last_row_date == expected_session_date and len(df) >= 2:
            # History đã có dòng của phiên giao dịch gần nhất.
            # Vì vậy giá tham chiếu phải là close của dòng trước đó, KHÔNG phải close của dòng mới nhất.
            previous_close = safe_float(df.iloc[-2]["close"])
            if realtime_price is None:
                realtime_price = latest_history_close
                pricing_mode = "history_current_session_vs_previous_session"
            else:
                # Cập nhật close hiện tại để chỉ báo gần realtime hơn.
                df.loc[df.index[-1], "close"] = realtime_price
                df.loc[df.index[-1], "high"] = max(safe_float(df.iloc[-1]["high"], realtime_price), realtime_price)
                df.loc[df.index[-1], "low"] = min(safe_float(df.iloc[-1]["low"], realtime_price), realtime_price)
                pricing_mode = "intraday_over_history_current_session_vs_previous_session"
        elif has_intraday:
            # Trong phiên mới nhưng history chưa có dòng hôm nay.
            # Khi đó dòng cuối history chính là giá đóng cửa phiên trước, dùng làm reference/previousClose.
            previous_close = latest_history_close
            pricing_mode = "intraday_vs_latest_history_close"
        else:
            # Không có intraday thì vẫn nên hiển thị biến động của phiên gần nhất:
            # latest close - previous session close. Tránh fallback currentPrice = previousClose làm priceChange = 0 giả.
            previous_close = safe_float(df.iloc[-2]["close"]) if len(df) >= 2 else None
            realtime_price = latest_history_close
            pricing_mode = "latest_history_close_vs_previous_session"

        if previous_close is None or previous_close == 0 or realtime_price is None:
            return {"error": f"Không đủ dữ liệu giá để phân tích mã {symbol_upper}"}, 442

        # Thêm chỉ báo sau khi đã cập nhật close nếu có dữ liệu intraday cùng phiên.
        df = add_technical_indicators(df)
        latest = df.iloc[-1]

        current_price = safe_float(realtime_price)
        display_current_price = round_price_vn(current_price)
        display_previous_close = round_price_vn(previous_close)

        if display_current_price is None or display_previous_close is None or display_previous_close == 0:
            return {"error": f"Không đủ dữ liệu giá để phân tích mã {symbol_upper}"}, 442

        # Tính biến động từ giá đã chuẩn hóa/hiển thị để UI không lệch số.
        price_change = display_current_price - display_previous_close
        percent_change = (price_change / display_previous_close) * 100

        if price_change > 0:
            status, color = "up", "green"
        elif price_change < 0:
            status, color = "down", "red"
        else:
            status, color = "unchanged", "yellow"

        technical = {
            "rsi14": round_number(latest.get("RSI"), 2),
            "ma20": round_price_vn(latest.get("MA20")),
            "ma50": round_price_vn(latest.get("MA50")),
            "ma100": round_price_vn(latest.get("MA100")),
            "ma200": round_price_vn(latest.get("MA200")),
            "macd": round_number(latest.get("MACD"), 2),
            "macdSignal": round_number(latest.get("Signal_Line"), 2),
            "macdHistogram": round_number(latest.get("MACD_Histogram"), 2),
            "volume": round_number(latest.get("volume"), 0),
            "avgVolume20": round_number(latest.get("avgVolume20"), 0),
            "bollingerUpper": round_price_vn(latest.get("Bollinger_Upper")),
            "bollingerLower": round_price_vn(latest.get("Bollinger_Lower")),
        }

        levels = find_support_resistance(df, current_price, lookback=120)
        risk_management = calculate_risk_management(current_price, technical, levels)
        market = analyze_vnindex_market()
        signal_result = analyze_signal(current_price, technical, levels, risk_management, market, df)
        suggested_order = build_suggested_order(
            signal_result["signal"]["action"], current_price, risk_management, levels, market
        )

        # Cảnh báo nếu MA200 chỉ là fallback do chưa đủ 200 phiên.
        warnings = signal_result["warnings"][:]
        if len(df) < 200:
            warnings.append("Dữ liệu chưa đủ 200 phiên nên MA200 chỉ mang tính tham khảo theo dữ liệu hiện có")
        if market.get("warning"):
            warnings.append(market.get("warning"))
        warnings = list(dict.fromkeys(warnings))

        # Chuẩn hóa dữ liệu chart 120 phiên gần nhất.
        chart_df = df.tail(120).copy()
        chart_df["time"] = chart_df["time"].dt.strftime("%Y-%m-%d")
        chart_cols = [
            "time", "open", "high", "low", "close", "volume",
            "MA20", "MA50", "MA100", "MA200", "RSI",
            "MACD", "Signal_Line", "MACD_Histogram",
            "Bollinger_Upper", "Bollinger_Lower", "avgVolume20",
        ]
        chart_df = chart_df[chart_cols].replace({np.nan: None})
        chart_data = chart_df.to_dict(orient="records")

        latest_time = latest["time"].strftime("%Y-%m-%d") if hasattr(latest["time"], "strftime") else str(latest["time"])

        response = {
            "symbol": symbol_upper,

            # Chuẩn camelCase cho frontend hiện tại.
            "currentPrice": display_current_price,
            "referencePrice": display_previous_close,
            "previousClose": display_previous_close,
            "priceChange": round_number(price_change, 2),
            "percentChange": round_number(percent_change, 2),
            "status": status,
            "color": color,
            "rsi": technical["rsi14"],
            "ma20": technical["ma20"],
            "data": chart_data,

            # Alias camelCase phổ biến để tránh frontend cũ/mới đọc lệch field.
            "change": round_number(price_change, 2),
            "changePercent": round_number(percent_change, 2),

            # Bổ sung snake_case nếu frontend/backend khác cần dùng.
            "current_price": display_current_price,
            "reference_price": display_previous_close,
            "previous_close": display_previous_close,
            "price_change": round_number(price_change, 2),
            "price_change_percent": round_number(percent_change, 2),

            # Giá cơ bản phiên mới nhất.
            "open": round_price_vn(latest.get("open")),
            "high": round_price_vn(latest.get("high")),
            "low": round_price_vn(latest.get("low")),
            "close": round_price_vn(latest.get("close")),
            "volume": round_number(latest.get("volume"), 0),
            "time": latest_time,

            # Metadata giúp debug khi Render/local khác múi giờ hoặc khác dữ liệu history/intraday.
            "pricingMeta": {
                "pricingMode": pricing_mode,
                "serverTimeVietnam": current_time.strftime("%Y-%m-%d %H:%M:%S %z"),
                "historyLastDate": str(last_row_date),
                "expectedSessionDate": str(expected_session_date),
                "hasIntraday": has_intraday,
                "latestHistoryClose": round_price_vn(latest_history_close),
            },

            "technical": technical,
            "levels": levels,
            "riskManagement": risk_management,
            "market": market,
            "signal": signal_result["signal"],
            "suggestedOrder": suggested_order,
            "reasons": signal_result["reasons"],
            "warnings": warnings,
        }

        print(
            f"[PRICE_DEBUG] {symbol_upper} mode={pricing_mode} "
            f"current={response['currentPrice']} previousClose={response['previousClose']} "
            f"change={response['priceChange']} pct={response['percentChange']} "
            f"historyLastDate={last_row_date} expectedSessionDate={expected_session_date} "
            f"hasIntraday={has_intraday}"
        )

        return response, 200

    except Exception as e:
        return {"error": f"Lỗi hệ thống Máy chủ Backend: {str(e)}"}, 500
