from datetime import datetime, timedelta

import numpy as np

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

def get_stock_analysis_data(symbol):
    try:
        if not symbol or symbol.strip() == "":
            return {"error": "Mã cổ phiếu không được để trống"}, 400

        symbol_upper = symbol.strip().upper()
        stock_api = Vnstock().stock(symbol=symbol_upper, source="VCI")

        current_time = datetime.now()
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
        today_date = current_time.date()

        if last_row_date == today_date and len(df) >= 2:
            previous_close = safe_float(df.iloc[-2]["close"])
            if realtime_price is None:
                realtime_price = safe_float(df.iloc[-1]["close"])
            else:
                # Cập nhật close hiện tại để chỉ báo gần realtime hơn.
                df.loc[df.index[-1], "close"] = realtime_price
                df.loc[df.index[-1], "high"] = max(safe_float(df.iloc[-1]["high"], realtime_price), realtime_price)
                df.loc[df.index[-1], "low"] = min(safe_float(df.iloc[-1]["low"], realtime_price), realtime_price)
        elif has_intraday:
            previous_close = safe_float(df.iloc[-1]["close"])
            # Không append dòng giả để tránh làm sai OHLCV; dùng giá realtime cho phân tích hiện tại.
        else:
            previous_close = safe_float(df.iloc[-1]["close"])
            realtime_price = previous_close

        if previous_close is None or previous_close == 0 or realtime_price is None:
            return {"error": f"Không đủ dữ liệu giá để phân tích mã {symbol_upper}"}, 442

        # Thêm chỉ báo sau khi đã cập nhật close nếu có dữ liệu intraday cùng ngày.
        df = add_technical_indicators(df)
        latest = df.iloc[-1]

        current_price = safe_float(realtime_price)
        price_change = current_price - previous_close
        percent_change = (price_change / previous_close) * 100 if previous_close else 0

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

            # Giữ field cũ để frontend cũ không lỗi
            "currentPrice": round_price_vn(current_price),
            "referencePrice": round_price_vn(previous_close),
            "previousClose": round_price_vn(previous_close),
            "priceChange": round_number(price_change, 2),
            "percentChange": round_number(percent_change, 2),
            "status": status,
            "color": color,
            "rsi": technical["rsi14"],
            "ma20": technical["ma20"],
            "data": chart_data,

            # Bổ sung snake_case nếu frontend/backend khác cần dùng
            "current_price": round_price_vn(current_price),
            "reference_price": round_price_vn(previous_close),
            "previous_close": round_price_vn(previous_close),
            "price_change": round_number(price_change, 2),
            "price_change_percent": round_number(percent_change, 2),

            # Giá cơ bản phiên mới nhất
            "open": round_price_vn(latest.get("open")),
            "high": round_price_vn(latest.get("high")),
            "low": round_price_vn(latest.get("low")),
            "close": round_price_vn(latest.get("close")),
            "volume": round_number(latest.get("volume"), 0),
            "time": latest_time,

            "technical": technical,
            "levels": levels,
            "riskManagement": risk_management,
            "market": market,
            "signal": signal_result["signal"],
            "suggestedOrder": suggested_order,
            "reasons": signal_result["reasons"],
            "warnings": warnings,
        }

        return response, 200

    except Exception as e:
        return {"error": f"Lỗi hệ thống Máy chủ Backend: {str(e)}"}, 500
