import pandas as pd


# ==========================================================
# HELPER CƠ BẢN
# ==========================================================

def safe_float(value, default=None):
    """Ép dữ liệu về float an toàn, tránh crash khi gặp NaN/None/string lỗi."""
    try:
        if value is None:
            return default
        if pd.isna(value):
            return default
        return float(value)
    except Exception:
        return default

def round_number(value, digits=2):
    value = safe_float(value)
    if value is None:
        return None
    return round(value, digits)

def round_price_vn(value):
    """
    Làm tròn giá theo bước giá phổ biến ở Việt Nam.
    Không biết sàn cụ thể nên dùng quy tắc gần đúng: <10k: 10đ, 10k-50k: 50đ, >=50k: 100đ.
    """
    value = safe_float(value)
    if value is None:
        return None
    if value < 10_000:
        tick = 10
    elif value < 50_000:
        tick = 50
    else:
        tick = 100
    return round(value / tick) * tick

def normalize_price_value(value, multiply_by_1000=True):
    """vnstock thường trả giá cổ phiếu theo đơn vị nghìn đồng, nên cần đổi sang VNĐ."""
    value = safe_float(value)
    if value is None:
        return None
    if multiply_by_1000 and abs(value) < 1000:
        return value * 1000
    return value
