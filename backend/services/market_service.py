from datetime import datetime, timedelta

try:
    from vnstock3 import Vnstock
except ImportError:
    from vnstock import Vnstock

from utils.dataframe_utils import prepare_ohlcv_dataframe
from utils.helpers import safe_float, round_number


# ==========================================================
# VNINDEX / THỊ TRƯỜNG CHUNG
# ==========================================================

def analyze_vnindex_market():
    """Phân tích nhanh VNINDEX. Nếu vnstock lỗi thì trả UNKNOWN, không làm app crash."""
    fallback = {
        "vnindexPrice": None,
        "vnindexChangePercent": None,
        "vnindexMa20": None,
        "vnindexTrend": "UNKNOWN",
        "marketCondition": "UNKNOWN",
        "warning": "Không lấy được dữ liệu thị trường chung",
    }

    try:
        current_time = datetime.now()
        start_date = (current_time - timedelta(days=365)).strftime("%Y-%m-%d")
        end_date = current_time.strftime("%Y-%m-%d")

        index_api = Vnstock().stock(symbol="VNINDEX", source="VCI")
        df_index = index_api.quote.history(start=start_date, end=end_date, interval="1D")
        df_index = prepare_ohlcv_dataframe(df_index, multiply_price_by_1000=False)

        if df_index is None or df_index.empty or len(df_index) < 2:
            return fallback

        df_index["MA20"] = df_index["close"].rolling(window=20, min_periods=1).mean()
        latest = df_index.iloc[-1]
        previous = df_index.iloc[-2]

        price = safe_float(latest["close"])
        prev_close = safe_float(previous["close"])
        ma20 = safe_float(latest["MA20"])
        change_percent = ((price - prev_close) / prev_close) * 100 if price is not None and prev_close else None

        if price is not None and ma20 is not None and price > ma20 and (change_percent is None or change_percent >= -0.3):
            trend = "UP"
            condition = "GOOD"
        elif price is not None and ma20 is not None and price < ma20 and (change_percent is None or change_percent < 0):
            trend = "DOWN"
            condition = "BAD"
        else:
            trend = "NEUTRAL"
            condition = "NORMAL"

        return {
            "vnindexPrice": round_number(price, 2),
            "vnindexChangePercent": round_number(change_percent, 2),
            "vnindexMa20": round_number(ma20, 2),
            "vnindexTrend": trend,
            "marketCondition": condition,
        }
    except Exception:
        return fallback
