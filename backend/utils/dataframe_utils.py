import numpy as np
import pandas as pd

from utils.helpers import normalize_price_value


OHLCV_COLUMNS = ["open", "high", "low", "close", "volume"]


def prepare_ohlcv_dataframe(df, multiply_price_by_1000=True):
    """
    Chuẩn hóa OHLCV từ vnstock về DataFrame an toàn:
    - time tăng dần
    - open/high/low/close/volume là số
    - thiếu open/high/low thì fallback bằng close để frontend không crash
    - thiếu volume thì fallback 0
    """
    if df is None or getattr(df, "empty", True):
        return pd.DataFrame()

    df = df.copy()

    if "time" not in df.columns:
        if "date" in df.columns:
            df = df.rename(columns={"date": "time"})
        elif "tradingDate" in df.columns:
            df = df.rename(columns={"tradingDate": "time"})
        else:
            return pd.DataFrame()

    df["time"] = pd.to_datetime(df["time"], errors="coerce")
    df = df.dropna(subset=["time"]).sort_values("time").drop_duplicates(subset=["time"]).reset_index(drop=True)

    for col in OHLCV_COLUMNS:
        if col not in df.columns:
            df[col] = np.nan
        df[col] = pd.to_numeric(df[col], errors="coerce")
        if col != "volume" and multiply_price_by_1000:
            df[col] = df[col].apply(lambda x: normalize_price_value(x, True))

    df = df.dropna(subset=["close"]).reset_index(drop=True)

    if df.empty:
        return pd.DataFrame()

    for col in ["open", "high", "low"]:
        df[col] = df[col].where(df[col].notna(), df["close"])

    df["volume"] = df["volume"].fillna(0).clip(lower=0)

    return df[["time", "open", "high", "low", "close", "volume"]]
