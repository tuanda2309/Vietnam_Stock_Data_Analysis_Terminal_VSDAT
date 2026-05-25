from __future__ import annotations

# Backward-compatible facade.
# Các module khác vẫn có thể import từ services.export_service như trước,
# còn phần xử lý thật đã được tách vào package services.export.*.

from .export.constants import EXCEL_MIME_TYPE
from .export.data_preparation import (
    _build_monthly_summary,
    _calculate_metrics,
    _prepare_analysis_dataframe,
    _risk_assessment,
    _rsi_comment,
    _trend_assessment,
)
from .export.excel_helpers import (
    _center_all_report_tables,
    _center_range,
    _clean_sheet_values,
    _copy_cell_style,
    _copy_row_style,
    _ensure_template_rows,
    _set_chart_series_title,
    _set_series_formula,
    _set_value,
    _set_workbook_calc_mode,
    _unmerge_ranges_from_row,
)
from .export.formatters import (
    _chart_date_text,
    _date_text,
    _format_percent_text,
    _format_price_text,
    _format_signed_percent_text,
    _format_signed_price_text,
    _format_volume_million_text,
    _month_text,
    _safe_float,
    _safe_value,
)
from .export.naming import _build_filename, _format_export_date_for_filename
from .export.service import create_excel_report
from .export.sheet_writers import (
    _write_analysis,
    _write_change_log,
    _write_clean_data,
    _write_dashboard,
    _write_data_issues,
    _write_executive_summary,
    _write_methodology,
)
from .export.stock_api import get_stock_api
from .export.template_loader import _load_template_workbook
from .export.workbook_builder import _build_excel_report_from_template

__all__ = [
    "EXCEL_MIME_TYPE",
    "create_excel_report",
    "get_stock_api",
]
