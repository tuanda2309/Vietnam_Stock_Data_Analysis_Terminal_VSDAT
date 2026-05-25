from __future__ import annotations

try:
    from vnstock3 import Vnstock
except ImportError:  # pragma: no cover
    from vnstock import Vnstock

from constants import SOURCE


def get_stock_api(symbol_upper: str):
    return Vnstock().stock(symbol=symbol_upper, source=SOURCE)
