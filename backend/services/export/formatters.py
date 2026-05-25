from __future__ import annotations

from typing import Any

import pandas as pd


def _safe_float(value: Any, default: float = 0.0) -> float:
    if value is None or pd.isna(value):
        return default
    return float(value)


def _safe_value(value: Any, default: Any = None) -> Any:
    if value is None or pd.isna(value):
        return default
    return value


def _date_text(value: Any) -> str:
    if value is None or pd.isna(value):
        return ""
    return pd.to_datetime(value).strftime("%d/%m/%Y")


def _month_text(value: Any) -> str:
    if value is None or pd.isna(value):
        return ""
    return pd.to_datetime(value).strftime("%Y-%m")


def _chart_date_text(value: Any) -> str:
    if value is None or pd.isna(value):
        return ""
    return pd.to_datetime(value).strftime("%d/%m")


def _format_price_text(value: Any) -> str:
    if value is None or pd.isna(value):
        return "N/A"
    return f"{float(value):,.0f}"


def _format_signed_price_text(value: Any) -> str:
    if value is None or pd.isna(value):
        return "N/A"
    number = float(value)
    sign = "+" if number > 0 else ""
    return f"{sign}{number:,.0f}"


def _format_percent_text(value: Any) -> str:
    if value is None or pd.isna(value):
        return "N/A"
    return f"{float(value) * 100:.2f}%"


def _format_signed_percent_text(value: Any) -> str:
    if value is None or pd.isna(value):
        return "N/A"
    number = float(value)
    sign = "+" if number > 0 else ""
    return f"{sign}{number * 100:.2f}%"


def _format_volume_million_text(value: Any) -> str:
    if value is None or pd.isna(value):
        return "N/A"
    return f"{float(value) / 1_000_000:.2f}"
