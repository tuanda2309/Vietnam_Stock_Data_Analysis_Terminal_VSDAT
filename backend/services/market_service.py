import logging
import threading
import time
from datetime import datetime, timedelta

from vnstock import Market

from utils.dataframe_utils import prepare_ohlcv_dataframe
from utils.helpers import safe_float, round_number


# ==========================================================
# VNINDEX / THỊ TRƯỜNG CHUNG
# ==========================================================

_LOGGER = logging.getLogger(__name__)
_VNINDEX_REFRESH_TTL_SECONDS = 15 * 60
_VNINDEX_RETRY_DELAY_SECONDS = 60
_VNINDEX_LOCK = threading.Lock()
_VNINDEX_CACHE = None
_VNINDEX_CACHE_UPDATED_AT = 0.0
_VNINDEX_NEXT_REFRESH_AT = 0.0
_VNINDEX_REFRESHING = False


def _unknown_market():
    return {
        "vnindexPrice": None,
        "vnindexChangePercent": None,
        "vnindexMa20": None,
        "vnindexTrend": "UNKNOWN",
        "marketCondition": "UNKNOWN",
        "warning": "Không lấy được dữ liệu thị trường chung",
    }


def _fetch_vnindex_market():
    """Tải và phân tích VNINDEX; chỉ chạy trong thread nền."""

    try:
        current_time = datetime.now()
        start_date = (current_time - timedelta(days=365)).strftime("%Y-%m-%d")
        end_date = current_time.strftime("%Y-%m-%d")

        # Use the configured index OHLCV route so DNSE can fail over to FHSC/SSI.
        index_api = Market().index("VNINDEX")
        df_index = index_api.ohlcv(start=start_date, end=end_date, interval="1D")
        df_index = prepare_ohlcv_dataframe(df_index, multiply_price_by_1000=False)

        if df_index is None or df_index.empty or len(df_index) < 2:
            return None

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
        _LOGGER.warning("Cannot fetch VNINDEX market context", exc_info=True)
        return None


def _refresh_vnindex_cache():
    global _VNINDEX_CACHE, _VNINDEX_CACHE_UPDATED_AT, _VNINDEX_NEXT_REFRESH_AT, _VNINDEX_REFRESHING

    try:
        result = _fetch_vnindex_market()
        if result is not None:
            with _VNINDEX_LOCK:
                _VNINDEX_CACHE = result
                _VNINDEX_CACHE_UPDATED_AT = time.monotonic()
        else:
            with _VNINDEX_LOCK:
                _VNINDEX_NEXT_REFRESH_AT = time.monotonic() + _VNINDEX_RETRY_DELAY_SECONDS
    finally:
        with _VNINDEX_LOCK:
            _VNINDEX_REFRESHING = False


def analyze_vnindex_market():
    """Return VNINDEX context, loading synchronously on a cold cache."""
    global _VNINDEX_NEXT_REFRESH_AT, _VNINDEX_REFRESHING

    now = time.monotonic()
    start_refresh = False
    wait_for_refresh = False

    with _VNINDEX_LOCK:
        if (
            _VNINDEX_CACHE is not None
            and now - _VNINDEX_CACHE_UPDATED_AT < _VNINDEX_REFRESH_TTL_SECONDS
        ):
            return dict(_VNINDEX_CACHE)

        if not _VNINDEX_REFRESHING and now >= _VNINDEX_NEXT_REFRESH_AT:
            _VNINDEX_REFRESHING = True
            _VNINDEX_NEXT_REFRESH_AT = now + _VNINDEX_REFRESH_TTL_SECONDS
            start_refresh = True
            wait_for_refresh = _VNINDEX_CACHE is None

        result = dict(_VNINDEX_CACHE) if _VNINDEX_CACHE is not None else _unknown_market()

    if start_refresh:
        if wait_for_refresh:
            _refresh_vnindex_cache()
        else:
            try:
                threading.Thread(
                    target=_refresh_vnindex_cache,
                    name="vnindex-refresh",
                    daemon=True,
                ).start()
            except RuntimeError:
                with _VNINDEX_LOCK:
                    _VNINDEX_REFRESHING = False
                _LOGGER.warning("Could not start VNINDEX background refresh", exc_info=True)

    if wait_for_refresh:
        with _VNINDEX_LOCK:
            result = dict(_VNINDEX_CACHE) if _VNINDEX_CACHE is not None else _unknown_market()

    return result
