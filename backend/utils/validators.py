import re
from datetime import datetime, timezone, timedelta


SYMBOL_PATTERN = re.compile(r"^[A-Z0-9]{1,10}$")
MAX_EXPORT_DAYS = 365 * 10
MAX_EXPORT_ROWS = 10000
VN_TZ = timezone(timedelta(hours=7))


def validate_symbol(symbol):
    """Validate và chuẩn hóa mã cổ phiếu do người dùng nhập."""
    if symbol is None or str(symbol).strip() == "":
        return None, "Mã cổ phiếu không được để trống"

    symbol_upper = str(symbol).strip().upper()

    if not SYMBOL_PATTERN.fullmatch(symbol_upper):
        return None, "Mã cổ phiếu không hợp lệ. Chỉ nhập chữ cái/số, tối đa 10 ký tự."

    return symbol_upper, None


def parse_yyyy_mm_dd(date_text, field_name):
    try:
        return datetime.strptime(date_text, "%Y-%m-%d")
    except (TypeError, ValueError):
        return None


def validate_date_range(start_date, end_date):
    """Validate khoảng ngày export theo mức an toàn production basic."""
    start_obj = parse_yyyy_mm_dd(start_date, "start_date")
    end_obj = parse_yyyy_mm_dd(end_date, "end_date")

    if start_obj is None or end_obj is None:
        return None, None, "Định dạng ngày không hợp lệ. Vui lòng dùng YYYY-MM-DD."

    if start_obj > end_obj:
        return None, None, "Ngày bắt đầu không được lớn hơn ngày kết thúc."

    today_vn = datetime.now(VN_TZ).replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=None)
    if start_obj > today_vn or end_obj > today_vn:
        return None, None, "Hệ thống không hỗ trợ trích xuất dữ liệu ngày tương lai."

    if (end_obj - start_obj).days > MAX_EXPORT_DAYS:
        return None, None, "Khoảng ngày xuất Excel quá dài. Vui lòng chọn tối đa 10 năm."

    return start_obj, end_obj, None
