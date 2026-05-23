import os
from datetime import datetime, timedelta, timezone

import numpy as np
import pandas as pd
from flask import current_app

try:
    from zoneinfo import ZoneInfo
except ImportError:
    ZoneInfo = None

try:
    from vnstock3 import Vnstock
except ImportError:
    from vnstock import Vnstock

from constants import DEFAULT_HISTORY_DAYS, SOURCE
from services.analysis_service import analyze_signal, build_suggested_order
from services.market_service import analyze_vnindex_market
from utils.dataframe_utils import prepare_ohlcv_dataframe
from utils.helpers import normalize_price_value, round_number, round_price_vn, safe_float
from utils.indicators import add_technical_indicators
from utils.json_utils import sanitize_for_json
from utils.risk import calculate_risk_management
from utils.simple_cache import cache_get, cache_set
from utils.support_resistance import find_support_resistance
from utils.validators import validate_symbol


try:
    VN_TZ = ZoneInfo("Asia/Ho_Chi_Minh") if ZoneInfo else timezone(timedelta(hours=7))
except Exception:
    VN_TZ = timezone(timedelta(hours=7))


def get_previous_weekday(day):
    day = day - timedelta(days=1)
    while day.weekday() >= 5:
        day = day - timedelta(days=1)
    return day


def get_expected_vietnam_trading_session_date(now_vn):
    session_day = now_vn.date()

    while session_day.weekday() >= 5:
        session_day = session_day - timedelta(days=1)

    if now_vn.weekday() < 5 and now_vn.hour < 9:
        session_day = get_previous_weekday(now_vn.date())

    return session_day


def get_stock_api(symbol_upper):
    return Vnstock().stock(symbol=symbol_upper, source=SOURCE)


def get_latest_intraday_price(stock_api):
    """Lấy giá intraday mới nhất nếu vnstock hỗ trợ. Lỗi API ngoài không làm backend crash."""
    try:
        intraday = stock_api.quote.intraday()
        if intraday is None or getattr(intraday, "empty", True) or "price" not in intraday.columns:
            return None, False

        intraday = intraday.copy()
        time_col = next((col for col in ["time", "datetime", "match_time", "tradingDate"] if col in intraday.columns), None)
        if time_col:
            intraday[time_col] = pd.to_datetime(intraday[time_col], errors="coerce")
            intraday = intraday.dropna(subset=[time_col]).sort_values(time_col)

        price = normalize_price_value(intraday.iloc[-1]["price"], True)
        if price is None or price <= 0:
            return None, False

        return price, True
    except Exception:
        current_app.logger.warning("Cannot fetch intraday price", exc_info=True)
        return None, False


def build_status(price_change):
    if price_change > 0:
        return "up", "green"
    if price_change < 0:
        return "down", "red"
    return "unchanged", "yellow"


def get_stock_analysis_data(symbol):
    symbol_upper, validation_error = validate_symbol(symbol)
    if validation_error:
        return {"error": validation_error}, 400

    cache_key = f"stock-analysis:{symbol_upper}"
    cached_response = cache_get(cache_key)
    if cached_response is not None:
        cached_response["cache"] = {"hit": True, "ttlSeconds": int(os.environ.get("STOCK_CACHE_TTL_SECONDS", "60"))}
        return cached_response, 200

    try:
        stock_api = get_stock_api(symbol_upper)
        current_time = datetime.now(VN_TZ)
        start_date = (current_time - timedelta(days=DEFAULT_HISTORY_DAYS)).strftime("%Y-%m-%d")
        end_date = current_time.strftime("%Y-%m-%d")

        try:
            raw_df = stock_api.quote.history(start=start_date, end=end_date, interval="1D")
        except Exception:
            current_app.logger.exception("Cannot fetch history data for %s", symbol_upper)
            return {"error": "Không lấy được dữ liệu chứng khoán từ nguồn bên ngoài. Vui lòng thử lại sau."}, 500

        df = prepare_ohlcv_dataframe(raw_df, multiply_price_by_1000=True)

        if df is None or df.empty:
            return {"error": f"Không tìm thấy dữ liệu giao dịch cho mã: {symbol_upper}"}, 404

        if len(df) < 20:
            return {"error": f"Dữ liệu cho mã {symbol_upper} quá ít để phân tích kỹ thuật."}, 400

        realtime_price, has_intraday = get_latest_intraday_price(stock_api)

        last_row_date = df.iloc[-1]["time"].date()
        expected_session_date = get_expected_vietnam_trading_session_date(current_time)
        latest_history_close = safe_float(df.iloc[-1]["close"])
        pricing_mode = "unknown"

        if last_row_date == expected_session_date and len(df) >= 2:
            previous_close = safe_float(df.iloc[-2]["close"])
            if realtime_price is None:
                realtime_price = latest_history_close
                pricing_mode = "history_current_session_vs_previous_session"
            else:
                df.loc[df.index[-1], "close"] = realtime_price
                df.loc[df.index[-1], "high"] = max(safe_float(df.iloc[-1]["high"], realtime_price), realtime_price)
                df.loc[df.index[-1], "low"] = min(safe_float(df.iloc[-1]["low"], realtime_price), realtime_price)
                pricing_mode = "intraday_over_history_current_session_vs_previous_session"
        elif has_intraday:
            previous_close = latest_history_close
            pricing_mode = "intraday_vs_latest_history_close"
        else:
            previous_close = safe_float(df.iloc[-2]["close"]) if len(df) >= 2 else None
            realtime_price = latest_history_close
            pricing_mode = "latest_history_close_vs_previous_session"

        if previous_close is None or previous_close <= 0 or realtime_price is None or realtime_price <= 0:
            return {"error": f"Không đủ dữ liệu giá để phân tích mã {symbol_upper}."}, 400

        df = add_technical_indicators(df)
        latest = df.iloc[-1]

        current_price = safe_float(realtime_price)
        display_current_price = round_price_vn(current_price)
        display_previous_close = round_price_vn(previous_close)

        if display_current_price is None or display_previous_close is None or display_previous_close == 0:
            return {"error": f"Không đủ dữ liệu giá để phân tích mã {symbol_upper}."}, 400

        price_change = display_current_price - display_previous_close
        percent_change = (price_change / display_previous_close) * 100
        status, color = build_status(price_change)

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
            signal_result["signal"].get("action"), current_price, risk_management, levels, market
        )

        warnings = list(signal_result.get("warnings", []))
        warnings.append("Nhận xét chỉ phục vụ học tập và phân tích dữ liệu, không phải khuyến nghị đầu tư.")
        if len(df) < 200:
            warnings.append("Dữ liệu chưa đủ 200 phiên nên MA200 chỉ mang tính tham khảo theo dữ liệu hiện có.")
        if market.get("warning"):
            warnings.append(market.get("warning"))
        warnings = list(dict.fromkeys(warnings))

        chart_df = df.tail(120).copy()
        chart_df["time"] = chart_df["time"].dt.strftime("%Y-%m-%d")
        chart_cols = [
            "time", "open", "high", "low", "close", "volume",
            "MA20", "MA50", "MA100", "MA200", "RSI",
            "MACD", "Signal_Line", "MACD_Histogram",
            "Bollinger_Upper", "Bollinger_Lower", "avgVolume20",
        ]
        chart_df = chart_df[chart_cols].replace([np.inf, -np.inf], np.nan).replace({np.nan: None})
        chart_data = chart_df.to_dict(orient="records")

        latest_time = latest["time"].strftime("%Y-%m-%d") if hasattr(latest["time"], "strftime") else str(latest["time"])

        response = {
            "symbol": symbol_upper,
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
            "change": round_number(price_change, 2),
            "changePercent": round_number(percent_change, 2),
            "current_price": display_current_price,
            "reference_price": display_previous_close,
            "previous_close": display_previous_close,
            "price_change": round_number(price_change, 2),
            "price_change_percent": round_number(percent_change, 2),
            "open": round_price_vn(latest.get("open")),
            "high": round_price_vn(latest.get("high")),
            "low": round_price_vn(latest.get("low")),
            "close": round_price_vn(latest.get("close")),
            "volume": round_number(latest.get("volume"), 0),
            "time": latest_time,
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
            "signal": signal_result.get("signal"),
            "suggestedOrder": suggested_order,
            "reasons": signal_result.get("reasons", []),
            "warnings": warnings,
            "cache": {"hit": False, "ttlSeconds": int(os.environ.get("STOCK_CACHE_TTL_SECONDS", "60"))},
        }

        response = sanitize_for_json(response)
        cache_set(cache_key, response, int(os.environ.get("STOCK_CACHE_TTL_SECONDS", "60")))

        current_app.logger.info(
            "Stock analysis ok symbol=%s mode=%s current=%s previous=%s change=%s pct=%s",
            symbol_upper,
            pricing_mode,
            response["currentPrice"],
            response["previousClose"],
            response["priceChange"],
            response["percentChange"],
        )

        return response, 200

    except Exception:
        current_app.logger.exception("Stock analysis failed for %s", symbol_upper)
        return {"error": "Lỗi hệ thống khi phân tích mã cổ phiếu. Vui lòng thử lại sau."}, 500
