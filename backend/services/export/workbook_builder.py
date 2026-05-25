from __future__ import annotations

from io import BytesIO

import pandas as pd

from .data_preparation import _build_monthly_summary, _calculate_metrics
from .excel_helpers import _center_all_report_tables, _set_workbook_calc_mode
from .sheet_writers import (
    _write_analysis,
    _write_change_log,
    _write_clean_data,
    _write_dashboard,
    _write_data_issues,
    _write_executive_summary,
    _write_methodology,
)
from .template_loader import _load_template_workbook


def _build_excel_report_from_template(symbol_upper: str, data: pd.DataFrame) -> BytesIO:
    wb = _load_template_workbook()

    expected_sheets = [
        "Executive Summary",
        "Dashboard quản trị",
        "Phân tích",
        "Dữ liệu sạch",
        "Data Issues",
        "Change Log",
        "Phương pháp",
    ]
    missing = [name for name in expected_sheets if name not in wb.sheetnames]
    if missing:
        raise ValueError(f"Template thiếu sheet bắt buộc: {', '.join(missing)}")

    metrics = _calculate_metrics(symbol_upper, data)
    monthly = _build_monthly_summary(data)

    _write_executive_summary(wb["Executive Summary"], metrics)
    _write_clean_data(wb["Dữ liệu sạch"], data)
    _write_analysis(wb["Phân tích"], metrics, data, monthly)
    _write_data_issues(wb["Data Issues"], data)
    _write_change_log(wb["Change Log"], metrics)
    _write_methodology(wb["Phương pháp"])
    _write_dashboard(wb["Dashboard quản trị"], metrics, monthly, len(data))
    _center_all_report_tables(wb, len(data), len(monthly))

    wb.active = wb.sheetnames.index("Executive Summary")
    wb.properties.title = f"Báo cáo cổ phiếu {symbol_upper}"
    wb.properties.subject = "Stock executive report"
    wb.properties.creator = "Stock Analytics System"
    wb.properties.keywords = f"{symbol_upper}, stock, report, dashboard"
    wb.properties.description = "Báo cáo Excel tự động tạo từ template đã duyệt, giữ layout giống bản gửi quản lý."
    _set_workbook_calc_mode(wb)

    output = BytesIO()
    wb.save(output)
    output.seek(0)
    return output
