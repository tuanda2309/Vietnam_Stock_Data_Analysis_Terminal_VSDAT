import pandas as pd
import numpy as np


# ==========================================================
# CHỈ BÁO KỸ THUẬT
# ==========================================================

def calculate_rsi(series, period=14):
    """RSI theo Wilder EMA, có fallback 50 khi dữ liệu phẳng hoặc thiếu."""
    series = pd.to_numeric(series, errors="coerce")
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = (-delta).clip(lower=0)

    avg_gain = gain.ewm(alpha=1 / period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / period, adjust=False).mean()

    rs = avg_gain / avg_loss.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))
    rsi = rsi.where(avg_loss != 0, 100)
    rsi = rsi.where(~((avg_gain == 0) & (avg_loss == 0)), 50)
    return rsi.fillna(50)

def calculate_macd(series, fast=12, slow=26, signal=9):
    series = pd.to_numeric(series, errors="coerce")
    ema_fast = series.ewm(span=fast, adjust=False).mean()
    ema_slow = series.ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    hist = macd_line - signal_line
    return macd_line, signal_line, hist

def calculate_bollinger_bands(series, window=20, num_sd=2):
    series = pd.to_numeric(series, errors="coerce")
    ma = series.rolling(window=window, min_periods=1).mean()
    sd = series.rolling(window=window, min_periods=2).std().fillna(0)
    upper_band = ma + (sd * num_sd)
    lower_band = ma - (sd * num_sd)
    return upper_band, lower_band

def add_technical_indicators(df):
    """Thêm MA, RSI, MACD, Bollinger, Volume trung bình. Có fallback khi chưa đủ MA200."""
    df = df.copy()
    close = df["close"]

    df["MA20"] = close.rolling(window=20, min_periods=1).mean()
    df["MA50"] = close.rolling(window=50, min_periods=1).mean()
    df["MA100"] = close.rolling(window=100, min_periods=1).mean()
    df["MA200"] = close.rolling(window=200, min_periods=1).mean()
    df["RSI"] = calculate_rsi(close, 14)

    macd_line, signal_line, hist = calculate_macd(close)
    df["MACD"] = macd_line
    df["Signal_Line"] = signal_line
    df["MACD_Histogram"] = hist

    upper, lower = calculate_bollinger_bands(close)
    df["Bollinger_Upper"] = upper
    df["Bollinger_Lower"] = lower

    df["avgVolume20"] = df["volume"].rolling(window=20, min_periods=1).mean()
    return df
