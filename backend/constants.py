import os

RISK_WARNING = "Dữ liệu chỉ phục vụ mục đích học tập và phân tích, không phải khuyến nghị đầu tư. Người dùng tự chịu trách nhiệm với quyết định của mình."

SOURCE = os.environ.get("VNSTOCK_SOURCE", "dnse").strip().lower()
DEFAULT_HISTORY_DAYS = 365 * 2
