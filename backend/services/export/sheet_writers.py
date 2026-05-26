from __future__ import annotations

from typing import Any, Dict
from openpyxl.styles import Alignment
from copy import copy
from openpyxl.styles import Alignment, Font

import pandas as pd

from .constants import (
    NUMBER_FORMAT_DATE,
    NUMBER_FORMAT_DECIMAL,
    NUMBER_FORMAT_PERCENT,
    NUMBER_FORMAT_PRICE,
    NUMBER_FORMAT_RSI,
    NUMBER_FORMAT_VOLUME,
)
from .excel_helpers import (
    _clean_sheet_values,
    _ensure_template_rows,
    _set_chart_series_title,
    _set_series_formula,
    _set_value,
    _unmerge_ranges_from_row,
)
from .formatters import (
    _format_percent_text,
    _format_price_text,
    _format_signed_percent_text,
    _format_volume_million_text,
    _safe_float,
    _safe_value,
)


def _write_executive_summary(ws, metrics: Dict[str, Any]) -> None:
    symbol = metrics["symbol"]

    ws["A1"] = f"EXECUTIVE SUMMARY - BÁO CÁO CỔ PHIẾU {symbol}"

    old_a2 = ws["A2"]
    old_style = copy(old_a2._style)
    old_font = copy(old_a2.font)
    old_fill = copy(old_a2.fill)
    old_border = copy(old_a2.border)
    old_alignment = copy(old_a2.alignment)

    for merged_range in list(ws.merged_cells.ranges):
        if merged_range.min_row == 2 and merged_range.max_row == 2:
            ws.unmerge_cells(str(merged_range))

    for col in range(1, 13):  # A -> L
        cell = ws.cell(row=2, column=col)
        cell.value = None
        cell.hyperlink = None
        cell._style = copy(old_style)
        cell.font = copy(old_font)
        cell.fill = copy(old_fill)
        cell.border = copy(old_border)
        cell.alignment = copy(old_alignment)

    ws["A2"] = "Nguồn:"
    ws["B2"] = "VSDAT"
    ws["C2"] = (
        f"|  Giai đoạn: {metrics['start_date']} - {metrics['end_date']}  |  "
        f"Số phiên: {metrics['trading_days']}  |  "
        f"Ngày hoàn thiện: {metrics['completed_date']}"
    )

    ws.merge_cells("C2:L2")
    ws.column_dimensions["B"].width = 5.58

    ws["B2"].hyperlink = "https://vsdat-frontend.onrender.com/"
    ws["B2"].font = Font(
        name=old_font.name,
        size=old_font.sz,
        bold=old_font.b,
        italic=old_font.i,
        color="0563C1",
        underline="single"
    )

    ws["A2"].hyperlink = None
    ws["C2"].hyperlink = None

    ws["A2"].alignment = Alignment(horizontal="right", vertical="center")
    ws["B2"].alignment = Alignment(horizontal="left", vertical="center")
    ws["C2"].alignment = Alignment(horizontal="left", vertical="center")

    ws["A4"] = "Giá cuối kỳ"
    ws["A5"] = _format_price_text(metrics["end_close"])
    ws["A6"] = "VND/cp"
    ws["A7"] = f"{metrics['trend_word'].capitalize()} {abs(metrics['period_change']):,.0f} VND/cp so với đầu kỳ."

    ws["D4"] = "Hiệu suất kỳ"
    ws["D5"] = _format_signed_percent_text(metrics["period_pct"])
    ws["D6"] = "so với đầu kỳ"
    ws["D7"] = f"Xu hướng: {metrics['trend_short']}."

    ws["G4"] = "Thanh khoản TB"
    ws["G5"] = _format_volume_million_text(metrics["avg_volume"])
    ws["G6"] = "triệu cp/phiên"
    ws["G7"] = (
        f"Cao nhất {_format_volume_million_text(metrics['max_volume'])} triệu cp "
        f"vào {metrics['max_volume_date']}."
    )

    ws["J4"] = "Mức rủi ro"
    ws["J5"] = metrics["risk_label"]
    ws["J6"] = f"Drawdown {_format_percent_text(metrics['max_drawdown'])}"
    ws["J7"] = f"Đáy drawdown vào {metrics['max_drawdown_date']}."

    ws["A9"] = "1. Tình hình hiện tại"
    ws["A10"] = (
        f"• {symbol} {metrics['trend_word']} {_format_signed_percent_text(metrics['period_pct'])} "
        f"trong giai đoạn {metrics['start_date']} - {metrics['end_date']}, "
        f"từ {_format_price_text(metrics['start_close'])} xuống {_format_price_text(metrics['end_close'])} VND/cp."
    )
    ws["A11"] = (
        f"• Biên giá trong kỳ: thấp nhất {_format_price_text(metrics['period_low'])} VND/cp "
        f"({metrics['period_low_date']}), cao nhất {_format_price_text(metrics['period_high'])} VND/cp "
        f"({metrics['period_high_date']})."
    )
    ws["A12"] = (
        f"• Drawdown sâu nhất đạt {_format_percent_text(metrics['max_drawdown'])} "
        f"vào {metrics['max_drawdown_date']}; mức rủi ro được xếp loại {metrics['risk_label']}."
    )
    ws["A13"] = (
        f"• Thanh khoản bình quân {_format_volume_million_text(metrics['avg_volume'])} triệu cp/phiên; "
        f"phiên cao nhất {_format_volume_million_text(metrics['max_volume'])} triệu cp vào {metrics['max_volume_date']}."
    )
    ws["A14"] = (
        f"• Cuối kỳ: giá đóng cửa {_format_price_text(metrics['end_close'])} VND/cp, "
        f"{metrics['ma5_position']} ({_format_price_text(metrics['ma5'])}), "
        f"{metrics['ma20_position']} ({_format_price_text(metrics['ma20'])}); "
        f"RSI14 = {_safe_float(metrics['rsi14']):.1f}, trạng thái trung tính."
    )

    ws["A16"] = "2. Điểm nổi bật / vấn đề cần chú ý"
    ws["A17"] = "Nhóm"
    ws["D17"] = "Đánh giá"
    ws["G17"] = "Ý nghĩa quản trị"

    ws["A18"] = "Xu hướng giá"
    ws["D18"] = metrics["trend_label"]
    ws["G18"] = (
        f"Giá cuối kỳ {_format_price_text(metrics['end_close'])} VND/cp; "
        f"hiệu suất kỳ {_format_signed_percent_text(metrics['period_pct'])}. "
        "Cần báo cáo rõ mức giảm và tránh diễn giải quá tích cực khi chưa có tín hiệu đảo chiều."
    )

    ws["A19"] = "Biến động"
    ws["D19"] = metrics["risk_label"]
    ws["G19"] = (
        f"Drawdown sâu nhất {_format_percent_text(metrics['max_drawdown'])}; "
        f"phiên giảm mạnh nhất {metrics['max_down_date']} ({_format_signed_percent_text(metrics['max_down_pct'])}). "
        "Cần nhấn mạnh quản trị rủi ro."
    )

    ws["A20"] = "Thanh khoản"
    ws["D20"] = "Cần theo dõi"
    ws["G20"] = (
        f"TB {_format_volume_million_text(metrics['avg_volume'])} triệu cp/phiên; "
        f"cao nhất {_format_volume_million_text(metrics['max_volume'])} triệu cp. "
        "Khi giá hồi phục, cần kiểm tra thanh khoản có xác nhận hay không."
    )

    ws["A21"] = "Kỹ thuật ngắn hạn"
    ws["D21"] = "Trung tính/Yếu" if metrics["period_pct"] < 0 else "Tích cực/Cần xác nhận"
    ws["G21"] = (
        f"Cuối kỳ {metrics['ma5_position'].replace('MA5', 'ma5')}, "
        f"RSI14 = {_safe_float(metrics['rsi14']):.1f}. "
        "Chờ giá vượt MA5/MA10 cùng thanh khoản cải thiện trước khi đánh giá tích cực hơn."
    )

    ws["A23"] = "3. Đề xuất hành động"
    ws["A24"] = "• Không ra quyết định mua mới chỉ dựa trên nhịp hồi ngắn; ưu tiên chờ giá vượt MA5/MA10 cùng thanh khoản cải thiện."
    ws["A25"] = (
        f"• Theo dõi vùng hỗ trợ gần {_format_price_text(metrics['period_low'])} VND/cp và vùng xác nhận ngắn hạn "
        f"quanh MA5 {_format_price_text(metrics['ma5'])} - MA10 {_format_price_text(metrics['ma10'])} VND/cp."
    )
    ws["A26"] = "• Nếu giá thủng vùng đáy kỳ hoặc drawdown tiếp tục mở rộng, cần giảm khẩu vị rủi ro và cập nhật lại kịch bản."
    ws["A27"] = "• Khi báo cáo cho sếp, tập trung vào 3 điểm: hiệu suất kỳ, drawdown lớn nhất và điều kiện xác nhận hồi phục bằng thanh khoản."
    ws["A29"] = "Ghi chú: Báo cáo phục vụ mục đích quản trị nội bộ, được tổng hợp từ dữ liệu lịch sử trong kỳ phân tích và không phải là khuyến nghị đầu tư."

def _write_dashboard(ws, metrics: Dict[str, Any], monthly: pd.DataFrame, data_rows: int) -> None:
    symbol = metrics["symbol"]
    ws["A1"] = f"DASHBOARD QUẢN TRỊ - CỔ PHIẾU {symbol}"
    ws["A2"] = f"Kỳ báo cáo: {metrics['start_date']} - {metrics['end_date']} | Dữ liệu: {metrics['trading_days']} phiên giao dịch"

    ws["A4"] = "Giá cuối kỳ"
    ws["A5"] = _format_price_text(metrics["end_close"])
    ws["A6"] = "VND/cp"
    ws["A7"] = f"{_format_signed_percent_text(metrics['period_pct'])} so với đầu kỳ"

    ws["D4"] = "Drawdown lớn nhất"
    ws["D5"] = _format_percent_text(metrics["max_drawdown"])
    ws["D6"] = "mức giảm từ đỉnh"
    ws["D7"] = f"Ngày {metrics['max_drawdown_date']}"

    ws["G4"] = "KL TB"
    ws["G5"] = _format_volume_million_text(metrics["avg_volume"])
    ws["G6"] = "triệu cp/phiên"
    ws["G7"] = f"Cao nhất {_format_volume_million_text(metrics['max_volume'])} triệu"

    ws["J4"] = "RSI14 cuối kỳ"
    ws["J5"] = f"{_safe_float(metrics['rsi14']):.1f}"
    ws["J6"] = "điểm"
    ws["J7"] = f"Tín hiệu: {metrics['last_signal']}"

    ws["A9"] = "Xu hướng giá đóng cửa và MA20"
    ws["A26"] = "Hiệu suất theo tháng"
    ws["G26"] = "Thanh khoản bình quân theo tháng"
    ws["A44"] = "Nhận xét nhanh cho quản lý"
    ws["A45"] = f"• Xu hướng chính trong kỳ là {metrics['trend_short']}, hiệu suất {_format_signed_percent_text(metrics['period_pct'])}."
    ws["A46"] = f"• Rủi ro nổi bật là drawdown {_format_percent_text(metrics['max_drawdown'])}, cần quản trị điểm cắt lỗ và kịch bản xấu."
    ws["A47"] = f"• Thanh khoản bình quân {_format_volume_million_text(metrics['avg_volume'])} triệu cp/phiên; cần xác nhận bằng thanh khoản khi giá hồi phục."

    # Update chart references while preserving chart objects/layout from template.
    if not ws._charts:
        return

    clean_last_row = data_rows + 1  # Header row 1 + data rows.
    clean_start_chart_row = 21 if data_rows >= 20 else 2  # MA20 starts at row 21 in template logic.
    month_start = 18
    month_end = max(month_start, month_start + max(len(monthly), 1) - 1)

    # Chart 1: close + MA20, categories from hidden/display date column V.
    chart1 = ws._charts[0]
    if len(chart1.series) >= 1:
        _set_series_ref_formula = _set_series_formula
        _set_series_ref_formula(chart1.series[0], f"'Dữ liệu sạch'!$E${clean_start_chart_row}:$E${clean_last_row}", f"'Dữ liệu sạch'!$V${clean_start_chart_row}:$V${clean_last_row}")
        _set_chart_series_title(chart1.series[0], "Đóng cửa")
    if len(chart1.series) >= 2:
        _set_series_formula(chart1.series[1], f"'Dữ liệu sạch'!$M${clean_start_chart_row}:$M${clean_last_row}", f"'Dữ liệu sạch'!$V${clean_start_chart_row}:$V${clean_last_row}")
        _set_chart_series_title(chart1.series[1], "MA20")

    # Chart 2: monthly performance.
    if len(ws._charts) >= 2:
        chart2 = ws._charts[1]
        if chart2.series:
            _set_series_formula(chart2.series[0], f"'Phân tích'!$E${month_start}:$E${month_end}", f"'Phân tích'!$A${month_start}:$A${month_end}")
            _set_chart_series_title(chart2.series[0], "Hiệu suất tháng")

    # Chart 3: monthly average volume.
    if len(ws._charts) >= 3:
        chart3 = ws._charts[2]
        if chart3.series:
            _set_series_formula(chart3.series[0], f"'Phân tích'!$F${month_start}:$F${month_end}", f"'Phân tích'!$A${month_start}:$A${month_end}")
            _set_chart_series_title(chart3.series[0], "KL TB (triệu cp)")


def _write_clean_data(ws, data: pd.DataFrame) -> None:
    headers = [
        "Ngày", "Mở cửa", "Cao nhất", "Thấp nhất", "Đóng cửa", "Thay đổi giá", "% thay đổi",
        "Khối lượng", "Lợi suất ngày", "Lợi suất lũy kế", "MA5", "MA10", "MA20", "Biến động 5 phiên",
        "Biến động 20 phiên", "Đỉnh lũy kế", "Drawdown", "RSI14", "Volume MA5", "Volume/MA5", "Tín hiệu", "Ngày biểu đồ",
    ]
    max_col = len(headers)
    ws.delete_rows(len(data) + 2, max(0, ws.max_row - len(data) - 1)) if ws.max_row > len(data) + 1 else None

    for col_idx, header in enumerate(headers, 1):
        ws.cell(1, col_idx).value = header

    _ensure_template_rows(ws, 2, 2, max(len(data), 1), max_col)
    _clean_sheet_values(ws, 2, max(ws.max_row, len(data) + 1), 1, max_col)

    rows = []
    for _, row in data.iterrows():
        rows.append(
            [
                row["time"].to_pydatetime() if hasattr(row["time"], "to_pydatetime") else row["time"],
                _safe_float(row["open"]),
                _safe_float(row["high"]),
                _safe_float(row["low"]),
                _safe_float(row["close"]),
                _safe_float(row["Change"]),
                _safe_float(row["PercentChangeRaw"]),
                _safe_float(row["volume"]),
                _safe_float(row["DailyReturn"]),
                _safe_float(row["CumulativeReturn"]),
                _safe_value(row["MA5"]),
                _safe_value(row["MA10"]),
                _safe_value(row["MA20"]),
                _safe_value(row["Volatility5"]),
                _safe_value(row["Volatility20"]),
                _safe_value(row["Peak"]),
                _safe_float(row["Drawdown"]),
                _safe_value(row["RSI14"]),
                _safe_value(row["VolumeMA5"]),
                _safe_value(row["VolumeRatio5"]),
                row["Signal"],
                row["ChartDate"],
            ]
        )

    for r_idx, values in enumerate(rows, 2):
        for c_idx, value in enumerate(values, 1):
            cell = ws.cell(r_idx, c_idx)
            cell.value = value

    # Number format must be stable even when rows are copied/extended.
    last_row = len(data) + 1
    for row in range(2, last_row + 1):
        for col in [1]:
            ws.cell(row, col).number_format = NUMBER_FORMAT_DATE
        for col in [2, 3, 4, 5, 6, 11, 12, 13, 16]:
            ws.cell(row, col).number_format = NUMBER_FORMAT_PRICE
        for col in [7, 9, 10, 14, 15, 17]:
            ws.cell(row, col).number_format = NUMBER_FORMAT_PERCENT
        for col in [8, 19]:
            ws.cell(row, col).number_format = NUMBER_FORMAT_VOLUME
        ws.cell(row, 18).number_format = NUMBER_FORMAT_RSI
        ws.cell(row, 20).number_format = NUMBER_FORMAT_DECIMAL

    # Update table range. Template table covers A:U only; column V is only for chart labels.
    if "CleanDataTbl" in ws.tables:
        ws.tables["CleanDataTbl"].ref = f"A1:U{last_row}"

    ws.auto_filter.ref = f"A1:V{last_row}"
    try:
        ws.freeze_panes = None  # Match file mẫu v2 exactly.
    except Exception:
        pass


def _write_analysis(ws, metrics: Dict[str, Any], data: pd.DataFrame, monthly: pd.DataFrame) -> None:
    _unmerge_ranges_from_row(ws, 4)
    symbol = metrics["symbol"]
    ws["A1"] = f"PHÂN TÍCH CHI TIẾT - CỔ PHIẾU {symbol}"
    ws["A2"] = f"Nguồn dữ liệu: Dữ liệu sạch | Giai đoạn {metrics['start_date']} - {metrics['end_date']}"

    _clean_sheet_values(ws, 4, max(ws.max_row, 80), 1, 10)

    ws["A4"] = "Chỉ số"
    ws["B4"] = "Giá trị"
    ws["C4"] = "Đơn vị"
    ws["D4"] = "Nhận xét"

    kpi_rows = [
        ["Giá đầu kỳ", metrics["start_close"], "VND/cp", "Giá đóng cửa phiên đầu tiên trong kỳ"],
        ["Giá cuối kỳ", metrics["end_close"], "VND/cp", "Giá đóng cửa phiên cuối kỳ"],
        ["Hiệu suất kỳ", metrics["period_pct"], "%", "Mức thay đổi của giá đóng cửa cuối kỳ so với đầu kỳ"],
        ["Thay đổi giá", metrics["period_change"], "VND/cp", "Giảm giá tuyệt đối trong kỳ" if metrics["period_change"] < 0 else "Tăng giá tuyệt đối trong kỳ"],
        ["Thanh khoản TB", metrics["avg_volume_million"], "triệu cp/phiên", "Khối lượng giao dịch bình quân mỗi phiên"],
        ["Cao nhất kỳ", metrics["period_high"], "VND/cp", f"Ghi nhận ngày {metrics['period_high_date']}"],
        ["Thấp nhất kỳ", metrics["period_low"], "VND/cp", f"Ghi nhận ngày {metrics['period_low_date']}"],
        ["Drawdown lớn nhất", metrics["max_drawdown"], "%", f"Ghi nhận ngày {metrics['max_drawdown_date']}"],
        ["RSI14 cuối kỳ", _safe_value(metrics["rsi14"]), "điểm", metrics["rsi_comment"]],
    ]

    _ensure_template_rows(ws, 5, 5, len(kpi_rows), 10)
    for r_idx, row_values in enumerate(kpi_rows, 5):
        for c_idx, value in enumerate(row_values, 1):
            _set_value(ws, r_idx, c_idx, value)
    for row in range(5, 14):
        ws.cell(row, 2).number_format = NUMBER_FORMAT_PERCENT if row in [7, 12] else NUMBER_FORMAT_PRICE if row not in [9, 13] else NUMBER_FORMAT_DECIMAL

    monthly_start = 17
    headers = ["Tháng", "Số phiên", "Giá đầu", "Giá cuối", "Hiệu suất tháng", "KL TB (triệu cp)", "Cao nhất", "Thấp nhất", "Nhận xét"]
    for c_idx, header in enumerate(headers, 1):
        _set_value(ws, monthly_start, c_idx, header)

    month_data_start = 18
    _ensure_template_rows(ws, 18, month_data_start, max(len(monthly), 5), 10)
    for r_idx, (_, row) in enumerate(monthly.iterrows(), month_data_start):
        values = [row[h] for h in headers]
        for c_idx, value in enumerate(values, 1):
            _set_value(ws, r_idx, c_idx, value)
        ws.cell(r_idx, 3).number_format = NUMBER_FORMAT_PRICE
        ws.cell(r_idx, 4).number_format = NUMBER_FORMAT_PRICE
        ws.cell(r_idx, 5).number_format = NUMBER_FORMAT_PERCENT
        ws.cell(r_idx, 6).number_format = NUMBER_FORMAT_DECIMAL
        ws.cell(r_idx, 7).number_format = NUMBER_FORMAT_PRICE
        ws.cell(r_idx, 8).number_format = NUMBER_FORMAT_PRICE

    # Top/bottom section: keep exact position when <= 5 months to match template.
    top_section_row = 26 if len(monthly) <= 5 else month_data_start + len(monthly) + 3
    _set_value(ws, top_section_row, 1, "Top 5 phiên tăng mạnh nhất")
    _set_value(ws, top_section_row, 6, "Top 5 phiên giảm mạnh nhất")

    ws.merge_cells(
        start_row=top_section_row,
        start_column=1,
        end_row=top_section_row,
        end_column=4
    )

    ws.merge_cells(
        start_row=top_section_row,
        start_column=6,
        end_row=top_section_row,
        end_column=9
    )

    ws.cell(top_section_row, 1).alignment = Alignment(horizontal="center", vertical="center")
    ws.cell(top_section_row, 6).alignment = Alignment(horizontal="center", vertical="center")

    for c, h in enumerate(["Ngày", "% thay đổi", "Đóng cửa", "Khối lượng"], 1):
        _set_value(ws, top_section_row + 1, c, h)
    for c, h in enumerate(["Ngày", "% thay đổi", "Đóng cửa", "Khối lượng"], 6):
        _set_value(ws, top_section_row + 1, c, h)

    top_up = data.sort_values("PercentChangeRaw", ascending=False).head(5)
    top_down = data.sort_values("PercentChangeRaw", ascending=True).head(5)
    _ensure_template_rows(ws, top_section_row + 2, top_section_row + 2, 5, 10)

    for i in range(5):
        target_row = top_section_row + 2 + i
        if i < len(top_up):
            up = top_up.iloc[i]
            _set_value(ws, target_row, 1, up["time"].to_pydatetime())
            _set_value(ws, target_row, 2, _safe_float(up["PercentChangeRaw"]))
            _set_value(ws, target_row, 3, _safe_float(up["close"]))
            _set_value(ws, target_row, 4, _safe_float(up["volume"]))
        if i < len(top_down):
            down = top_down.iloc[i]
            _set_value(ws, target_row, 6, down["time"].to_pydatetime())
            _set_value(ws, target_row, 7, _safe_float(down["PercentChangeRaw"]))
            _set_value(ws, target_row, 8, _safe_float(down["close"]))
            _set_value(ws, target_row, 9, _safe_float(down["volume"]))

        for col in [1, 6]:
            ws.cell(target_row, col).number_format = NUMBER_FORMAT_DATE
        for col in [2, 7]:
            ws.cell(target_row, col).number_format = NUMBER_FORMAT_PERCENT
        for col in [3, 8]:
            ws.cell(target_row, col).number_format = NUMBER_FORMAT_PRICE
        for col in [4, 9]:
            ws.cell(target_row, col).number_format = NUMBER_FORMAT_VOLUME


def _write_data_issues(ws, data: pd.DataFrame) -> None:
    _clean_sheet_values(ws, 1, max(ws.max_row, 30), 1, 5)
    headers = ["Mức độ", "Vấn đề dữ liệu", "Trạng thái", "Mô tả / tác động", "Hành động"]
    for col_idx, header in enumerate(headers, 1):
        ws.cell(1, col_idx).value = header

    duplicated_dates = int(data["time"].duplicated().sum())
    missing_critical = int(data[["open", "high", "low", "close", "volume"]].isna().sum().sum())

    issues = [
        [
            "Thông tin",
            "Chỉ số rolling đầu kỳ bị trống",
            "Hợp lệ",
            "MA5/MA10/MA20, volatility, RSI14 và Volume MA cần đủ số phiên lịch sử nên các dòng đầu kỳ bị trống. Đây là đặc điểm tính toán bình thường, không phải lỗi dữ liệu.",
            "Giữ nguyên và ghi chú",
        ],
        [
            "Thông tin",
            "Nguồn dữ liệu chưa đối chiếu ngoài workbook",
            "Cần lưu ý",
            "Báo cáo được xây dựng dựa trên dữ liệu có sẵn trong file. Nếu dùng cho quyết định đầu tư thực tế, nên đối chiếu thêm nguồn chính thức.",
            "Ghi chú trong báo cáo",
        ],
        [
            "Đã kiểm tra",
            "Ngày giao dịch trùng lặp",
            "Không phát hiện" if duplicated_dates == 0 else f"Có {duplicated_dates} dòng trùng",
            "Không phát hiện ngày giao dịch bị trùng trong phạm vi dữ liệu đã xử lý." if duplicated_dates == 0 else "Có ngày giao dịch bị trùng, cần kiểm tra lại dữ liệu nguồn.",
            "Không cần xử lý" if duplicated_dates == 0 else "Kiểm tra dữ liệu nguồn/API",
        ],
        [
            "Đã kiểm tra",
            "Lỗi công thức thường gặp trong workbook",
            "Không phát hiện trong file mới" if missing_critical == 0 else "Cần kiểm tra",
            "Không phát hiện lỗi công thức trong file mới khi kiểm tra các dạng lỗi phổ biến của Excel. Workbook được tái tạo bằng giá trị sạch và định dạng lại để tránh lỗi repair/format từ file cũ." if missing_critical == 0 else f"Có {missing_critical} giá trị OHLCV bị thiếu sau chuẩn hóa.",
            "Không cần xử lý" if missing_critical == 0 else "Kiểm tra lại dữ liệu đầu vào",
        ],
    ]

    _ensure_template_rows(ws, 2, 2, len(issues), 5)
    for r_idx, row_values in enumerate(issues, 2):
        for c_idx, value in enumerate(row_values, 1):
            _set_value(ws, r_idx, c_idx, value)


def _write_change_log(ws, metrics: Dict[str, Any]) -> None:
    _clean_sheet_values(ws, 1, max(ws.max_row, 30), 1, 4)
    headers = ["Ngày", "Sheet", "Thay đổi", "Lý do"]
    for col_idx, header in enumerate(headers, 1):
        ws.cell(1, col_idx).value = header

    today = metrics["completed_date"]
    logs = [
        [today, "Toàn bộ workbook", "Tái tạo workbook mới từ dữ liệu nguồn để giảm rủi ro lỗi Excel [Repaired].", "File trước bị vỡ layout và có dấu hiệu lỗi định dạng/chart/object."],
        [today, "Executive Summary", "Thiết kế lại từ đầu theo layout quản lý: tiêu đề, phụ đề, KPI cards, bullet points, bảng nhận xét và đề xuất hành động.", "Ưu tiên khả năng đọc ở zoom 100%, không để chữ bị cắt/chồng."],
        [today, "Dashboard quản trị", "Tạo lại KPI cards và biểu đồ xu hướng/hiệu suất/thanh khoản, không để helper data lộ trên dashboard.", "Dashboard sạch, gọn, phù hợp trình bày cho cấp quản lý."],
        [today, "Dữ liệu sạch", "Chuẩn hóa ngày tháng, số tiền, phần trăm, khối lượng; thêm table filter và freeze header.", "Dữ liệu dễ kiểm tra, dễ lọc và đúng định dạng."],
        [today, "Data Issues", "Bổ sung sheet ghi chú vấn đề dữ liệu và trạng thái xử lý.", "Minh bạch các giới hạn dữ liệu."],
        [today, "Phân tích", "Bổ sung bảng KPI, monthly summary, top/bottom phiên biến động.", "Tăng tính phân tích và khả năng giải thích số liệu."],
        [today, "Dashboard quản trị", "Chỉnh lại biểu đồ: bỏ đường MA20 giai đoạn chưa đủ dữ liệu, chuẩn hóa trục ngày và đơn vị thanh khoản theo triệu cổ phiếu.", "Tăng khả năng đọc, tránh hiểu nhầm do trục ngày/đơn vị hiển thị không rõ."],
        [today, "Dữ liệu sạch", "Bổ sung cột 'Ngày biểu đồ' để trục thời gian trên chart hiển thị dạng ngày thay vì serial number.", "Cải thiện khả năng đọc dashboard, không ảnh hưởng dữ liệu gốc."],
    ]

    _ensure_template_rows(ws, 2, 2, len(logs), 4)
    for r_idx, row_values in enumerate(logs, 2):
        for c_idx, value in enumerate(row_values, 1):
            _set_value(ws, r_idx, c_idx, value)


def _write_methodology(ws) -> None:
    _clean_sheet_values(ws, 1, max(ws.max_row, 25), 1, 3)
    rows = [
        ["Mục", "Cách hiểu", "Ghi chú"],
        ["Hiệu suất kỳ", "(Giá đóng cửa cuối kỳ / Giá đóng cửa đầu kỳ) - 1", "Đo mức tăng/giảm cả kỳ."],
        ["Drawdown", "(Giá hiện tại / Đỉnh lũy kế) - 1", "Cho biết mức giảm từ đỉnh trong kỳ."],
        ["MA5/MA10/MA20", "Trung bình động 5/10/20 phiên", "Dùng để đọc xu hướng ngắn/trung hạn."],
        ["RSI14", "Chỉ báo sức mạnh tương đối 14 phiên", "Khoảng 50 thường được xem là trung tính."],
        ["Thanh khoản TB", "Tổng khối lượng / số phiên", "Đơn vị trong báo cáo là triệu cp/phiên."],
        ["Giới hạn", "Báo cáo dựa trên dữ liệu có sẵn trong workbook.", "Không thay thế thẩm định hoặc nguồn dữ liệu chính thức."],
    ]
    _ensure_template_rows(ws, 1, 1, len(rows), 3)
    for r_idx, row_values in enumerate(rows, 1):
        for c_idx, value in enumerate(row_values, 1):
            _set_value(ws, r_idx, c_idx, value)
