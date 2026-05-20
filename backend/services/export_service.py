from io import BytesIO
from datetime import datetime

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
from openpyxl.cell.rich_text import TextBlock, CellRichText
from openpyxl.cell.text import InlineFont
from openpyxl.styles.colors import Color
import pandas as pd

try:
    from vnstock3 import Vnstock
except ImportError:
    from vnstock import Vnstock

from config import DEVELOPER_EMAIL, DEVELOPER_PHONE, DEVELOPER_GITHUB, DEVELOPER_WEB
from utils.dataframe_utils import prepare_ohlcv_dataframe


# ==========================================================
# API XUẤT FILE BÁO CÁO EXCEL - GIỮ CHỨC NĂNG CŨ
# ==========================================================

def create_excel_report(symbol, start_date, end_date):
    try:
        if not symbol or symbol.strip() == "":
            return None, None, {"error": "Mã cổ phiếu không được để trống"}, 400

        symbol_upper = symbol.strip().upper()

        try:
            start_obj = datetime.strptime(start_date, "%Y-%m-%d")
            end_obj = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            return None, None, {"error": "Định dạng ngày không hợp lệ. Vui lòng dùng YYYY-MM-DD"}, 400

        if start_obj > end_obj:
            return None, None, {"error": "Ngày bắt đầu không được lớn hơn ngày kết thúc"}, 400

        if start_obj > datetime.now() or end_obj > datetime.now():
            return None, None, {"error": "Hệ thống không hỗ trợ trích xuất dữ liệu ngày tương lai"}, 400

        stock_api = Vnstock().stock(symbol=symbol_upper, source="VCI")
        df = stock_api.quote.history(start=start_date, end=end_date, interval="1D")
        df = prepare_ohlcv_dataframe(df, multiply_price_by_1000=True)

        if df is None or df.empty:
            return None, None, {"error": f"Không có dữ liệu lịch sử để xuất file cho mã {symbol_upper}"}, 442

        df["Change"] = df["close"].diff().fillna(0)
        df["PercentChange"] = (df["close"].pct_change() * 100).fillna(0)
        df = df[df["time"] >= pd.to_datetime(start_date)].reset_index(drop=True)

        wb = Workbook()
        ws = wb.active
        ws.title = symbol_upper

        normal_font = Font(name="Arial", size=8)
        header_font = Font(name="Arial", size=8, color="FFFFFF", bold=True)
        blue_fill = PatternFill(start_color="0066CC", end_color="0066CC", fill_type="solid")
        center = Alignment(horizontal="center", vertical="center")

        inline_bold = InlineFont(rFont="Arial", sz=8, b=True)
        inline_normal = InlineFont(rFont="Arial", sz=8, b=False)
        inline_link = InlineFont(rFont="Arial", sz=8, b=False, u="single", color=Color(rgb="0000FF"))

        ws["A1"] = CellRichText([TextBlock(inline_bold, "Email: "), TextBlock(inline_normal, DEVELOPER_EMAIL)])
        ws["A2"] = CellRichText([TextBlock(inline_bold, "Phone: "), TextBlock(inline_normal, DEVELOPER_PHONE)])

        ws["A3"] = CellRichText([TextBlock(inline_bold, "GitHub: "), TextBlock(inline_link, "Tại đây")])
        ws["A3"].hyperlink = DEVELOPER_GITHUB
        ws["A3"].style = "Hyperlink"

        ws["A4"] = CellRichText([TextBlock(inline_bold, "Web: "), TextBlock(inline_link, "Tại đây")])
        ws["A4"].hyperlink = DEVELOPER_WEB
        ws["A4"].style = "Hyperlink"

        headers = [
            "NGÀY", "GIÁ MỞ CỬA", "GIÁ CAO NHẤT", "GIÁ THẤP NHẤT",
            "GIÁ ĐÓNG CỬA", "THAY ĐỔI GIÁ", "% THAY ĐỔI", "KHỐI LƯỢNG",
        ]
        header_row = 5

        for col_num, header in enumerate(headers, 1):
            cell = ws.cell(row=header_row, column=col_num)
            cell.value = header
            cell.fill = blue_fill
            cell.font = header_font
            cell.alignment = center

        data_start_row = 6
        for row_num, (_, row) in enumerate(df.iterrows(), data_start_row):
            values = [
                row["time"].strftime("%d/%m/%Y"),
                float(row["open"]), float(row["high"]), float(row["low"]), float(row["close"]),
                float(row["Change"]), float(row["PercentChange"]), float(row["volume"]),
            ]

            for col_num, value in enumerate(values, 1):
                cell = ws.cell(row=row_num, column=col_num, value=value)
                cell.font = normal_font
                cell.alignment = center

                if col_num in [2, 3, 4, 5, 6]:
                    cell.number_format = "#,##0.00"
                elif col_num == 7:
                    cell.number_format = "0.00"
                elif col_num == 8:
                    cell.number_format = "#,##0"

        for column in ws.columns:
            max_length = 0
            column_letter = get_column_letter(column[0].column)
            for cell in column:
                try:
                    if cell.value and not isinstance(cell.value, CellRichText):
                        max_length = max(max_length, len(str(cell.value)))
                except Exception:
                    pass
            ws.column_dimensions[column_letter].width = max_length + 5

        ws.column_dimensions["A"].width = 14

        excel_file = BytesIO()
        wb.save(excel_file)
        excel_file.seek(0)

        filename = f"{symbol_upper}_{start_date}_{end_date}.xlsx"
        return excel_file, filename, None, 200

    except Exception as e:
        return None, None, {"error": f"Lỗi xuất tệp Excel hệ thống: {str(e)}"}, 500
