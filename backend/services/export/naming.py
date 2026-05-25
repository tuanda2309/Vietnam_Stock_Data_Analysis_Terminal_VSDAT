from __future__ import annotations

from typing import Any

import pandas as pd


def _format_export_date_for_filename(value: Any) -> str:
    """Format ngày cho tên file export theo đúng dạng ngày_tháng_năm."""
    return pd.to_datetime(value).strftime("%d_%m_%Y")


def _build_filename(symbol_upper: str, start_date: Any, end_date: Any) -> str:
    clean_symbol = str(symbol_upper).upper().strip().replace("_VSDAT", "").replace("-VSDAT", "")
    safe_start = _format_export_date_for_filename(start_date)
    safe_end = _format_export_date_for_filename(end_date)
    return f"{clean_symbol}_{safe_start}_{safe_end}.xlsx"
