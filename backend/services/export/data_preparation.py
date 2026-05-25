from __future__ import annotations

from typing import Any, Dict

import pandas as pd

from .formatters import _chart_date_text, _date_text, _safe_float, _safe_value


def _prepare_analysis_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()
    data["time"] = pd.to_datetime(data["time"])
    data = data.sort_values("time").reset_index(drop=True)

    required_cols = ["time", "open", "high", "low", "close", "volume"]
    for col in required_cols:
        if col not in data.columns:
            raise ValueError(f"Thiếu cột dữ liệu bắt buộc: {col}")

    numeric_cols = ["open", "high", "low", "close", "volume"]
    for col in numeric_cols:
        data[col] = pd.to_numeric(data[col], errors="coerce")

    data = data.dropna(subset=["time", "open", "high", "low", "close", "volume"]).reset_index(drop=True)

    data["Change"] = data["close"].diff().fillna(0)
    data["PercentChangeRaw"] = data["close"].pct_change().replace([float("inf"), float("-inf")], 0).fillna(0)
    data["DailyReturn"] = data["PercentChangeRaw"]

    first_close = _safe_float(data["close"].iloc[0]) if not data.empty else 0
    data["CumulativeReturn"] = data["close"] / first_close - 1 if first_close else 0

    data["MA5"] = data["close"].rolling(window=5).mean()
    data["MA10"] = data["close"].rolling(window=10).mean()
    data["MA20"] = data["close"].rolling(window=20).mean()
    data["Volatility5"] = data["DailyReturn"].rolling(window=5).std()
    data["Volatility20"] = data["DailyReturn"].rolling(window=20).std()

    data["Peak"] = data["close"].cummax()
    data["Drawdown"] = (data["close"] / data["Peak"] - 1).replace([float("inf"), float("-inf")], 0).fillna(0)

    diff = data["close"].diff()
    gain = diff.clip(lower=0)
    loss = -diff.clip(upper=0)
    avg_gain_14 = gain.rolling(window=14).mean()
    avg_loss_14 = loss.rolling(window=14).mean()
    rs14 = avg_gain_14 / avg_loss_14.replace(0, pd.NA)
    data["RSI14"] = 100 - (100 / (1 + rs14))
    data.loc[(avg_loss_14 == 0) & (avg_gain_14 > 0), "RSI14"] = 100
    data.loc[(avg_loss_14 == 0) & (avg_gain_14 == 0), "RSI14"] = 50

    data["VolumeMA5"] = data["volume"].rolling(window=5).mean()
    data["VolumeRatio5"] = (data["volume"] / data["VolumeMA5"]).replace([float("inf"), float("-inf")], 0).fillna(0)

    def signal(row):
        ma5 = row.get("MA5")
        if ma5 is None or pd.isna(ma5):
            return "Chưa đủ dữ liệu"
        return "Trên MA5" if row["close"] >= ma5 else "Dưới MA5"

    data["Signal"] = data.apply(signal, axis=1)
    data["ChartDate"] = data["time"].apply(_chart_date_text)

    return data


def _trend_assessment(period_pct: float) -> str:
    if period_pct >= 0.10:
        return "Tăng mạnh"
    if period_pct >= 0.03:
        return "Tăng"
    if period_pct > -0.03:
        return "Ổn định"
    if period_pct > -0.10:
        return "Giảm"
    return "Giảm mạnh"


def _risk_assessment(max_drawdown: float, avg_abs_change: float) -> str:
    if abs(max_drawdown) >= 0.15 or avg_abs_change >= 0.035:
        return "Cao"
    if abs(max_drawdown) >= 0.07 or avg_abs_change >= 0.02:
        return "Trung bình"
    return "Thấp"


def _rsi_comment(rsi: Any) -> str:
    if rsi is None or pd.isna(rsi):
        return "Chưa đủ dữ liệu"
    value = float(rsi)
    if value >= 70:
        return "Vùng cao"
    if value <= 30:
        return "Vùng thấp"
    return "Trung tính quanh 50"


def _calculate_metrics(symbol_upper: str, data: pd.DataFrame) -> Dict[str, Any]:
    first = data.iloc[0]
    last = data.iloc[-1]

    start_close = _safe_float(first["close"])
    end_close = _safe_float(last["close"])
    period_change = end_close - start_close
    period_pct = period_change / start_close if start_close else 0

    high_idx = data["high"].idxmax()
    low_idx = data["low"].idxmin()
    max_volume_idx = data["volume"].idxmax()
    max_up_idx = data["PercentChangeRaw"].idxmax()
    max_down_idx = data["PercentChangeRaw"].idxmin()
    max_drawdown_idx = data["Drawdown"].idxmin()

    max_drawdown = _safe_float(data.loc[max_drawdown_idx, "Drawdown"])
    avg_abs_change = _safe_float(data["PercentChangeRaw"].abs().mean())

    ma5 = _safe_value(last.get("MA5"))
    ma10 = _safe_value(last.get("MA10"))
    ma20 = _safe_value(last.get("MA20"))
    rsi14 = _safe_value(last.get("RSI14"))

    def ma_position(ma_value, ma_name):
        if ma_value is None or pd.isna(ma_value):
            return f"chưa đủ dữ liệu {ma_name}"
        return f"trên {ma_name}" if end_close >= float(ma_value) else f"dưới {ma_name}"

    trend_label = _trend_assessment(period_pct)
    risk_label = _risk_assessment(max_drawdown, avg_abs_change)

    return {
        "symbol": symbol_upper,
        "start_date": _date_text(data["time"].min()),
        "end_date": _date_text(data["time"].max()),
        "trading_days": int(len(data)),
        "completed_date": pd.Timestamp.now().strftime("%d/%m/%Y"),
        "start_close": start_close,
        "end_close": end_close,
        "period_change": period_change,
        "period_pct": period_pct,
        "period_high": _safe_float(data.loc[high_idx, "high"]),
        "period_high_date": _date_text(data.loc[high_idx, "time"]),
        "period_low": _safe_float(data.loc[low_idx, "low"]),
        "period_low_date": _date_text(data.loc[low_idx, "time"]),
        "avg_volume": _safe_float(data["volume"].mean()),
        "avg_volume_million": _safe_float(data["volume"].mean()) / 1_000_000,
        "max_volume": _safe_float(data.loc[max_volume_idx, "volume"]),
        "max_volume_date": _date_text(data.loc[max_volume_idx, "time"]),
        "max_up_date": _date_text(data.loc[max_up_idx, "time"]),
        "max_up_pct": _safe_float(data.loc[max_up_idx, "PercentChangeRaw"]),
        "max_down_date": _date_text(data.loc[max_down_idx, "time"]),
        "max_down_pct": _safe_float(data.loc[max_down_idx, "PercentChangeRaw"]),
        "max_drawdown": max_drawdown,
        "max_drawdown_date": _date_text(data.loc[max_drawdown_idx, "time"]),
        "avg_abs_change": avg_abs_change,
        "ma5": ma5,
        "ma10": ma10,
        "ma20": ma20,
        "rsi14": rsi14,
        "rsi_comment": _rsi_comment(rsi14),
        "last_signal": last.get("Signal", ""),
        "ma5_position": ma_position(ma5, "MA5"),
        "ma10_position": ma_position(ma10, "MA10"),
        "ma20_position": ma_position(ma20, "MA20"),
        "trend_label": trend_label,
        "risk_label": risk_label,
        "trend_word": "tăng" if period_change >= 0 else "giảm",
        "trend_short": "tăng" if period_change >= 0 else "giảm mạnh" if period_pct <= -0.10 else "giảm",
    }


def _build_monthly_summary(data: pd.DataFrame) -> pd.DataFrame:
    temp = data.copy()
    temp["Month"] = temp["time"].dt.strftime("%Y-%m")
    rows = []
    for month, group in temp.groupby("Month", sort=True):
        first = group.iloc[0]
        last = group.iloc[-1]
        start_price = _safe_float(first["close"])
        end_price = _safe_float(last["close"])
        monthly_return = end_price / start_price - 1 if start_price else 0
        if monthly_return > 0.01:
            comment = "Tăng"
        elif monthly_return < -0.01:
            comment = "Giảm"
        else:
            comment = "Ổn định"
        rows.append(
            {
                "Tháng": month,
                "Số phiên": int(len(group)),
                "Giá đầu": start_price,
                "Giá cuối": end_price,
                "Hiệu suất tháng": monthly_return,
                "KL TB (triệu cp)": _safe_float(group["volume"].mean()) / 1_000_000,
                "Cao nhất": _safe_float(group["high"].max()),
                "Thấp nhất": _safe_float(group["low"].min()),
                "Nhận xét": comment,
            }
        )
    return pd.DataFrame(rows)
