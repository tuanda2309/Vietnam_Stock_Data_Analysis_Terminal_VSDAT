from __future__ import annotations

from vnstock import Market


def get_stock_api(symbol_upper: str):
    # Use Vnstock's configured OHLCV route so exports share the same source
    # failover as stock analysis instead of pinning every request to DNSE.
    return Market().equity(symbol_upper)
