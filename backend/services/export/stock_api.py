from __future__ import annotations

from vnstock import Market

from constants import SOURCE


def get_stock_api(symbol_upper: str):
    return Market(SOURCE).equity(symbol_upper)
