import pandas as pd
import numpy as np

from utils.helpers import normalize_price_value


def prepare_ohlcv_dataframe(df, multiply_price_by_1000=True):
    """Chuẩn hóa dữ liệu OHLCV từ vnstock về dạng tăng dần theo thời gian và số thực."""
    if df is None or df.empty:
        return pd.DataFrame()

    df = df.copy()
    if "time" not in df.columns:
        if "date" in df.columns:
            df = df.rename(columns={"date": "time"})
        else:
            return pd.DataFrame()

    df["time"] = pd.to_datetime(df["time"], errors="coerce")
    df = df.dropna(subset=["time"]).sort_values("time").reset_index(drop=True)

    for col in ["open", "high", "low", "close", "volume"]:
        if col not in df.columns:
            df[col] = np.nan
        df[col] = pd.to_numeric(df[col], errors="coerce")
        if col != "volume" and multiply_price_by_1000:
            df[col] = df[col].apply(lambda x: normalize_price_value(x, True))

    df = df.dropna(subset=["close"]).reset_index(drop=True)
    return df
