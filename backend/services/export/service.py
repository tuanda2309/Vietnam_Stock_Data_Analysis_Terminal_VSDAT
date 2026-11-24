from __future__ import annotations

from datetime import timedelta

import pandas as pd
from flask import current_app

from utils.dataframe_utils import prepare_ohlcv_dataframe
from utils.validators import MAX_EXPORT_ROWS, validate_date_range, validate_symbol

from .data_preparation import _prepare_analysis_dataframe
from .naming import _build_filename
from .stock_api import get_stock_api
from .workbook_builder import _build_excel_report_from_template


def _fetch_ohlcv_in_chunks(stock_api, start_obj, end_obj):
    """Fetch long export ranges in bounded, inclusive date windows."""
    cursor = start_obj.date()
    final_day = end_obj.date()
    frames = []
    # Keep each provider request below roughly 500 trading sessions while
    # avoiding too many sequential calls for a ten-year export.
    chunk_days = 730

    while cursor <= final_day:
        chunk_end = min(cursor + timedelta(days=chunk_days - 1), final_day)
        current_app.logger.info("Fetching export OHLCV %s to %s", cursor, chunk_end)
        frame = stock_api.ohlcv(
            start=cursor.isoformat(),
            end=chunk_end.isoformat(),
            interval="1D",
        )
        if frame is not None and not frame.empty:
            frames.append(frame)
        cursor = chunk_end + timedelta(days=1)

    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)


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
            raw_df = _fetch_ohlcv_in_chunks(stock_api, start_obj, end_obj)
        except Exception:
            current_app.logger.exception(
                "Không lấy được dữ liệu lịch sử cho mã %s trong khoảng %s đến %s",
                symbol_upper,
                start_date,
                end_date,
            )
            return (
                None,
                None,
                {"error": "Không lấy được dữ liệu chứng khoán từ nguồn bên ngoài. Vui lòng thử lại sau."},
                500,
            )

        df = prepare_ohlcv_dataframe(raw_df, multiply_price_by_1000=True)
        if df is None or df.empty:
            return None, None, {"error": f"Không có dữ liệu lịch sử để xuất file cho mã {symbol_upper}."}, 404

        df["time"] = pd.to_datetime(df["time"], errors="coerce")
        # vnstock may return Asia/Ho_Chi_Minh-aware timestamps. Strip the timezone
        # while keeping the local trading date so it can be filtered against the
        # user's date-only inputs and written to Excel.
        if isinstance(df["time"].dtype, pd.DatetimeTZDtype):
            df["time"] = df["time"].dt.tz_localize(None)

        start_ts = pd.Timestamp(start_obj)
        end_exclusive = pd.Timestamp(end_obj) + pd.Timedelta(days=1)
        df = df[
            (df["time"] >= start_ts) & (df["time"] < end_exclusive)
        ].reset_index(drop=True)
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
