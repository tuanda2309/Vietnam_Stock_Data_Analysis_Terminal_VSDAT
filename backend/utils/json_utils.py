import math

import numpy as np
import pandas as pd


def sanitize_for_json(value):
    """Chuyển NaN/Inf/numpy scalar/Timestamp thành kiểu JSON an toàn cho Flask jsonify."""
    if value is None:
        return None

    if isinstance(value, (pd.Timestamp,)):
        return value.strftime("%Y-%m-%d")

    if isinstance(value, (np.integer,)):
        return int(value)

    if isinstance(value, (np.floating,)):
        value = float(value)

    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return None
        return value

    if isinstance(value, dict):
        return {key: sanitize_for_json(val) for key, val in value.items()}

    if isinstance(value, list):
        return [sanitize_for_json(item) for item in value]

    if isinstance(value, tuple):
        return [sanitize_for_json(item) for item in value]

    return value
