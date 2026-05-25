from __future__ import annotations

import base64
from io import BytesIO

from openpyxl import load_workbook

from .constants import EMBEDDED_TEMPLATE_XLSX_B64


def _load_template_workbook():
    """
    Load workbook từ template nhúng sẵn trong code.

    Lý do: khi deploy lên Render/VPS/hosting, backend không còn phụ thuộc vào
    file stock_report_template.xlsx nằm ngoài source code. Frontend chỉ cần gọi
    API /export/... là tải file Excel về ngay.
    """
    template_bytes = base64.b64decode(EMBEDDED_TEMPLATE_XLSX_B64)
    return load_workbook(BytesIO(template_bytes))
