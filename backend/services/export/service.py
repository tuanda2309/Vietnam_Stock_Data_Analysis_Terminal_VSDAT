from __future__ import annotations

import pandas as pd
from flask import current_app

from utils.dataframe_utils import prepare_ohlcv_dataframe
from utils.validators import MAX_EXPORT_ROWS, validate_date_range, validate_symbol

from .data_preparation import _prepare_analysis_dataframe
from .naming import _build_filename
from .stock_api import get_stock_api
from .workbook_builder import _build_excel_report_from_template


def create_excel_report(symbol: str, start_date: str, end_date: str):
    """
    Router gọi trực tiếp hàm này.

    Return:
        excel_file, filename, error, status_code
    """
    try:
        symbol_upper, symbol_error = validate_symbol(symbol)
        if symbol_error:
            return None, None, {"error": symbol_error}, 400

        start_obj, end_obj, date_error = validate_date_range(start_date, end_date)
        if date_error:
            return None, None, {"error": date_error}, 400

        try:
            stock_api = get_stock_api(symbol_upper)
            raw_df = stock_api.quote.history(start=start_date, end=end_date, interval="1D")
        except Exception:
            current_app.logger.exception("Không lấy được dữ liệu lịch sử cho mã %s", symbol_upper)
            return (
                None,
                None,
                {"error": "Không lấy được dữ liệu chứng khoán từ nguồn bên ngoài. Vui lòng thử lại sau."},
                500,
            )

        df = prepare_ohlcv_dataframe(raw_df, multiply_price_by_1000=True)
        if df is None or df.empty:
            return None, None, {"error": f"Không có dữ liệu lịch sử để xuất file cho mã {symbol_upper}."}, 404

        df["time"] = pd.to_datetime(df["time"])
        df = df[(df["time"] >= pd.to_datetime(start_obj)) & (df["time"] <= pd.to_datetime(end_obj))].reset_index(drop=True)
        if df.empty:
            return None, None, {"error": f"Không có dữ liệu trong khoảng ngày đã chọn cho mã {symbol_upper}."}, 404

        if len(df) > MAX_EXPORT_ROWS:
            return (
                None,
                None,
                {"error": f"Dữ liệu export vượt quá {MAX_EXPORT_ROWS} dòng. Vui lòng chọn khoảng ngày ngắn hơn."},
                400,
            )

        data = _prepare_analysis_dataframe(df)
        if data.empty:
            return None, None, {"error": f"Dữ liệu sau chuẩn hóa bị trống cho mã {symbol_upper}."}, 404

        excel_file = _build_excel_report_from_template(symbol_upper, data)
        filename = _build_filename(symbol_upper, start_obj, end_obj)
        return excel_file, filename, None, 200

    except FileNotFoundError as exc:
        current_app.logger.exception("Excel template not found")
        return None, None, {"error": str(exc)}, 500
    except Exception:
        current_app.logger.exception("Excel export failed")
        return None, None, {"error": "Lỗi hệ thống khi xuất Excel. Vui lòng thử lại sau."}, 500
