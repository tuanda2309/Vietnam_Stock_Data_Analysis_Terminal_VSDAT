import os
from io import BytesIO
from datetime import datetime, timedelta

from flask import Flask, jsonify, send_file
from flask_cors import CORS
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
from openpyxl.cell.rich_text import TextBlock, CellRichText
from openpyxl.cell.text import InlineFont
from openpyxl.styles.colors import Color
import pandas as pd
import numpy as np

try:
    from vnstock3 import Vnstock
except ImportError:
    from vnstock import Vnstock

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

DEVELOPER_EMAIL = os.environ.get("DEVELOPER_EMAIL", "doananhtuan77qn@gmail.com")
DEVELOPER_PHONE = os.environ.get("DEVELOPER_PHONE", "0399848871")
DEVELOPER_GITHUB = os.environ.get("DEVELOPER_GITHUB", "https://github.com/tuanda2309")
DEVELOPER_WEB = os.environ.get("DEVELOPER_WEB", "https://vsdat-frontend.onrender.com")

RISK_WARNING = "Thông tin chỉ mang tính tham khảo, không phải khuyến nghị đầu tư. Người dùng cần tự chịu trách nhiệm với quyết định giao dịch."


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


# ==========================================================
# HỖ TRỢ / KHÁNG CỰ
# ==========================================================

def find_support_resistance(df, current_price, lookback=120):
    """
    Tìm hỗ trợ/kháng cự gần nhất bằng pivot low/high đơn giản.
    Nếu không có pivot phù hợp thì fallback bằng min/max 60 phiên gần nhất.
    """
    result = {
        "supportNearest": None,
        "resistanceNearest": None,
        "distanceToSupportPercent": None,
        "distanceToResistancePercent": None,
    }

    current_price = safe_float(current_price)
    if current_price is None or df is None or df.empty:
        return result

    recent = df.tail(lookback).copy().reset_index(drop=True)
    if recent.empty:
        return result

    lows = recent["low"].astype(float).values
    highs = recent["high"].astype(float).values

    pivot_lows = []
    pivot_highs = []
    for i in range(2, len(recent) - 2):
        if lows[i] <= lows[i - 1] and lows[i] <= lows[i - 2] and lows[i] <= lows[i + 1] and lows[i] <= lows[i + 2]:
            pivot_lows.append(lows[i])
        if highs[i] >= highs[i - 1] and highs[i] >= highs[i - 2] and highs[i] >= highs[i + 1] and highs[i] >= highs[i + 2]:
            pivot_highs.append(highs[i])

    supports = [x for x in pivot_lows if x <= current_price * 1.01]
    resistances = [x for x in pivot_highs if x >= current_price * 0.99]

    if supports:
        support = max(supports)
    else:
        support = recent.tail(min(60, len(recent)))["low"].min()

    if resistances:
        resistance = min(resistances)
    else:
        resistance = recent.tail(min(60, len(recent)))["high"].max()

    support = safe_float(support)
    resistance = safe_float(resistance)

    if support is not None:
        result["supportNearest"] = round_price_vn(support)
        result["distanceToSupportPercent"] = round_number(((current_price - support) / current_price) * 100, 2)

    if resistance is not None:
        result["resistanceNearest"] = round_price_vn(resistance)
        result["distanceToResistancePercent"] = round_number(((resistance - current_price) / current_price) * 100, 2)

    return result


# ==========================================================
# QUẢN TRỊ RỦI RO
# ==========================================================

def calculate_risk_management(current_price, technical, levels):
    """Sinh vùng mua, stop loss, take profit và Risk/Reward tham khảo."""
    price = safe_float(current_price)
    ma20 = safe_float(technical.get("ma20"))
    support = safe_float(levels.get("supportNearest"))
    resistance = safe_float(levels.get("resistanceNearest"))

    if price is None:
        return {
            "entryZone": {"from": None, "to": None},
            "stopLoss": None,
            "takeProfitZone": {"from": None, "to": None},
            "riskRewardRatio": None,
        }

    if support is None:
        support = price * 0.97
    if ma20 is None:
        ma20 = price
    if resistance is None or resistance <= price:
        resistance = price * 1.08

    if price > ma20:
        entry_from = min(support, ma20)
        entry_to = max(support, ma20) * 1.02
        entry_to = min(entry_to, price * 0.995) if price > entry_to else entry_to
    else:
        entry_from = min(price, support) * 0.995
        entry_to = min(ma20, price * 1.01)

    if entry_to < entry_from:
        entry_from, entry_to = entry_to * 0.98, entry_from

    stop_loss = support * 0.975
    take_profit_from = resistance
    if take_profit_from <= entry_to:
        take_profit_from = entry_to * 1.08
    take_profit_to = max(take_profit_from * 1.02, entry_to * 1.12)

    entry_mid = (entry_from + entry_to) / 2
    risk = entry_mid - stop_loss
    reward = take_profit_from - entry_mid
    rr = reward / risk if risk > 0 and reward > 0 else None

    return {
        "entryZone": {
            "from": round_price_vn(entry_from),
            "to": round_price_vn(entry_to),
        },
        "stopLoss": round_price_vn(stop_loss),
        "takeProfitZone": {
            "from": round_price_vn(take_profit_from),
            "to": round_price_vn(take_profit_to),
        },
        "riskRewardRatio": round_number(rr, 2),
    }


# ==========================================================
# VNINDEX / THỊ TRƯỜNG CHUNG
# ==========================================================

def analyze_vnindex_market():
    """Phân tích nhanh VNINDEX. Nếu vnstock lỗi thì trả UNKNOWN, không làm app crash."""
    fallback = {
        "vnindexPrice": None,
        "vnindexChangePercent": None,
        "vnindexMa20": None,
        "vnindexTrend": "UNKNOWN",
        "marketCondition": "UNKNOWN",
        "warning": "Không lấy được dữ liệu thị trường chung",
    }

    try:
        current_time = datetime.now()
        start_date = (current_time - timedelta(days=365)).strftime("%Y-%m-%d")
        end_date = current_time.strftime("%Y-%m-%d")

        index_api = Vnstock().stock(symbol="VNINDEX", source="VCI")
        df_index = index_api.quote.history(start=start_date, end=end_date, interval="1D")
        df_index = prepare_ohlcv_dataframe(df_index, multiply_price_by_1000=False)

        if df_index is None or df_index.empty or len(df_index) < 2:
            return fallback

        df_index["MA20"] = df_index["close"].rolling(window=20, min_periods=1).mean()
        latest = df_index.iloc[-1]
        previous = df_index.iloc[-2]

        price = safe_float(latest["close"])
        prev_close = safe_float(previous["close"])
        ma20 = safe_float(latest["MA20"])
        change_percent = ((price - prev_close) / prev_close) * 100 if price is not None and prev_close else None

        if price is not None and ma20 is not None and price > ma20 and (change_percent is None or change_percent >= -0.3):
            trend = "UP"
            condition = "GOOD"
        elif price is not None and ma20 is not None and price < ma20 and (change_percent is None or change_percent < 0):
            trend = "DOWN"
            condition = "BAD"
        else:
            trend = "NEUTRAL"
            condition = "NORMAL"

        return {
            "vnindexPrice": round_number(price, 2),
            "vnindexChangePercent": round_number(change_percent, 2),
            "vnindexMa20": round_number(ma20, 2),
            "vnindexTrend": trend,
            "marketCondition": condition,
        }
    except Exception:
        return fallback


# ==========================================================
# CHẤM ĐIỂM TÍN HIỆU / LỆNH GỢI Ý
# ==========================================================

def get_signal_text(action):
    mapping = {
        "BUY": {
            "title": "Có thể xem xét mua",
            "summary": "Cổ phiếu có nhiều tín hiệu kỹ thuật tích cực, nhưng vẫn cần quản trị rủi ro.",
        },
        "WATCH": {
            "title": "Chờ điểm mua đẹp hơn",
            "summary": "Tín hiệu chưa đủ mạnh để mua ngay. Nên chờ giá về vùng mua hoặc breakout rõ ràng.",
        },
        "HOLD": {
            "title": "Có thể tiếp tục nắm giữ",
            "summary": "Xu hướng chưa xấu, chưa có tín hiệu bán rõ ràng. Nếu chưa có cổ phiếu thì nên hiểu là theo dõi, không mua vội.",
        },
        "SELL": {
            "title": "Cân nhắc giảm tỷ trọng",
            "summary": "Một số tín hiệu kỹ thuật đang yếu đi. Nên thận trọng và không mua đuổi.",
        },
        "CUT_LOSS": {
            "title": "Cảnh báo cắt lỗ",
            "summary": "Giá đã vi phạm vùng rủi ro hoặc thủng hỗ trợ quan trọng. Cần ưu tiên bảo toàn vốn.",
        },
    }
    return mapping.get(action, mapping["WATCH"])


def classify_action(score):
    if score >= 75:
        return "BUY"
    if score >= 60:
        return "WATCH"
    if score >= 45:
        return "HOLD"
    if score >= 30:
        return "SELL"
    return "CUT_LOSS"


def analyze_signal(current_price, technical, levels, risk_management, market, df):
    """
    Chấm điểm tín hiệu 0-100 theo trend, RSI, MACD, volume, S/R, VNINDEX, R:R.
    Đây là logic tham khảo cho học tập, không phải khuyến nghị đầu tư.
    """
    price = safe_float(current_price)
    ma20 = safe_float(technical.get("ma20"))
    ma50 = safe_float(technical.get("ma50"))
    ma200 = safe_float(technical.get("ma200"))
    rsi = safe_float(technical.get("rsi14"))
    macd = safe_float(technical.get("macd"))
    macd_signal = safe_float(technical.get("macdSignal"))
    macd_hist = safe_float(technical.get("macdHistogram"))
    volume = safe_float(technical.get("volume"))
    avg_volume20 = safe_float(technical.get("avgVolume20"))
    support = safe_float(levels.get("supportNearest"))
    resistance = safe_float(levels.get("resistanceNearest"))
    dist_support = safe_float(levels.get("distanceToSupportPercent"))
    dist_resistance = safe_float(levels.get("distanceToResistancePercent"))
    stop_loss = safe_float(risk_management.get("stopLoss"))
    rr = safe_float(risk_management.get("riskRewardRatio"))

    score = 0
    reasons = []
    warnings = []

    # A. Xu hướng giá: 25 điểm
    if price is not None and ma20 is not None and price > ma20:
        score += 8
        reasons.append("Giá hiện tại cao hơn MA20")
    else:
        warnings.append("Giá đang dưới MA20 hoặc chưa xác nhận xu hướng ngắn hạn")

    if price is not None and ma50 is not None and price > ma50:
        score += 8
        reasons.append("Giá hiện tại cao hơn MA50")
    else:
        warnings.append("Giá chưa vượt MA50 nên xu hướng trung hạn chưa thật sự mạnh")

    if ma20 is not None and ma50 is not None and ma20 > ma50:
        score += 6
        reasons.append("MA20 đang nằm trên MA50, xu hướng ngắn hạn tích cực")

    if price is not None and ma200 is not None and price > ma200:
        score += 3
        reasons.append("Giá vẫn nằm trên MA200")

    # B. RSI: 15 điểm
    if rsi is not None:
        if 50 <= rsi <= 65:
            score += 15
            reasons.append(f"RSI {round(rsi, 2)} nằm trong vùng khỏe")
        elif 40 <= rsi < 50:
            score += 9
            reasons.append(f"RSI {round(rsi, 2)} ở vùng trung bình, cần theo dõi thêm")
        elif 65 < rsi <= 70:
            score += 9
            warnings.append(f"RSI {round(rsi, 2)} hơi cao, hạn chế mua đuổi")
        elif rsi > 70:
            score += 5
            warnings.append(f"RSI {round(rsi, 2)} trên 70, có rủi ro quá mua")
        elif 30 <= rsi < 40:
            score += 4
            warnings.append(f"RSI {round(rsi, 2)} dưới 40, lực giá còn yếu")
        else:
            score += 3
            warnings.append(f"RSI {round(rsi, 2)} dưới 30, quá bán nhưng chưa nên mua nếu chưa có tín hiệu hồi")

    # C. MACD: 15 điểm
    if macd is not None and macd_signal is not None:
        if macd > macd_signal:
            score += 8
            reasons.append("MACD đang cao hơn Signal")
        else:
            warnings.append("MACD đang thấp hơn Signal")

    if macd_hist is not None:
        if macd_hist > 0:
            score += 4
            reasons.append("MACD Histogram đang dương")
        else:
            warnings.append("MACD Histogram chưa tích cực")

    try:
        if df is not None and len(df) >= 2:
            prev_hist = safe_float(df.iloc[-2]["MACD_Histogram"])
            if prev_hist is not None and macd_hist is not None and macd_hist > prev_hist:
                score += 3
                reasons.append("MACD Histogram đang cải thiện so với phiên trước")
    except Exception:
        pass

    # D. Volume: 15 điểm
    strong_volume = False
    if volume is not None and avg_volume20 is not None and avg_volume20 > 0:
        if volume > avg_volume20 * 1.2:
            score += 15
            strong_volume = True
            reasons.append("Volume cao hơn trung bình 20 phiên, dòng tiền đang tốt")
        elif volume >= avg_volume20:
            score += 10
            reasons.append("Volume đạt mức trung bình 20 phiên")
        elif volume >= avg_volume20 * 0.7:
            score += 5
            warnings.append("Volume thấp hơn trung bình 20 phiên, tín hiệu chưa thật sự xác nhận")
        else:
            warnings.append("Volume yếu, không nên mua mạnh dù chỉ báo khác đẹp")

    # E. Hỗ trợ / kháng cự: 15 điểm
    breakout = False
    if price is not None and resistance is not None and price > resistance and strong_volume:
        score += 15
        breakout = True
        reasons.append("Giá vượt kháng cự kèm volume mạnh, có dấu hiệu breakout")
    else:
        if dist_support is not None:
            if 0 <= dist_support <= 3:
                score += 8
                reasons.append("Giá đang gần hỗ trợ, có vùng quản trị rủi ro rõ hơn")
            elif 3 < dist_support <= 6:
                score += 5
                reasons.append("Giá cách hỗ trợ không quá xa")
            elif dist_support > 10:
                warnings.append("Giá đã cách khá xa hỗ trợ, mua mới có thể không đẹp")

        if dist_resistance is not None:
            if dist_resistance > 8:
                score += 7
                reasons.append("Khoảng cách tới kháng cự còn tương đối rộng")
            elif dist_resistance > 5:
                score += 5
                reasons.append("Khoảng cách tới kháng cự còn chấp nhận được")
            elif dist_resistance >= 0:
                warnings.append("Giá đang gần kháng cự, không nên mua đuổi")

    # F. VNINDEX: 10 điểm
    market_condition = market.get("marketCondition")
    vnindex_trend = market.get("vnindexTrend")
    if market_condition == "GOOD" or vnindex_trend == "UP":
        score += 10
        reasons.append("VNINDEX đang ủng hộ xu hướng tăng")
    elif market_condition == "NORMAL" or vnindex_trend == "NEUTRAL":
        score += 5
        warnings.append("VNINDEX trung tính, nên quan sát thêm thị trường chung")
    elif market_condition == "BAD" or vnindex_trend == "DOWN":
        warnings.append("VNINDEX đang yếu, cần giảm tỷ trọng rủi ro")
    else:
        score += 3
        warnings.append("Chưa có dữ liệu thị trường chung để xác nhận")

    # G. Risk/Reward: 5 điểm
    if rr is not None:
        if rr >= 2:
            score += 5
            reasons.append(f"Risk/Reward khoảng {rr}, tương đối hấp dẫn")
        elif rr >= 1.5:
            score += 3
            reasons.append(f"Risk/Reward khoảng {rr}, tạm chấp nhận")
        else:
            warnings.append("Risk/Reward chưa hấp dẫn, không nên mua vội")
    else:
        warnings.append("Chưa đủ dữ liệu để tính Risk/Reward")

    # Điều kiện ưu tiên rủi ro
    if price is not None and stop_loss is not None and price < stop_loss:
        score = min(score, 25)
        warnings.append("Giá đã thủng stop loss tham khảo")
    elif price is not None and support is not None and price < support * 0.98:
        score = min(score, 28)
        warnings.append("Giá thủng hỗ trợ mạnh, ưu tiên quản trị rủi ro")
    elif price is not None and support is not None and price < support:
        score = min(score, 38)
        warnings.append("Giá đã thủng hỗ trợ gần nhất")

    if rsi is not None and rsi > 70 and dist_resistance is not None and 0 <= dist_resistance <= 3:
        score = min(score, 70)
        warnings.append("RSI quá mua và giá gần kháng cự, không nên phát tín hiệu BUY mạnh")

    if volume is not None and avg_volume20 is not None and volume < avg_volume20 and score >= 75 and not breakout:
        score = 72
        warnings.append("Volume chưa xác nhận nên hạ tín hiệu từ BUY xuống WATCH")

    score = int(max(0, min(100, round(score))))
    action = classify_action(score)

    if price is not None and stop_loss is not None and price < stop_loss:
        action = "CUT_LOSS"
    elif price is not None and support is not None and price < support * 0.98:
        action = "CUT_LOSS"
    elif rsi is not None and rsi > 70 and dist_resistance is not None and 0 <= dist_resistance <= 3 and action == "BUY":
        action = "WATCH"

    text = get_signal_text(action)
    warnings.append(RISK_WARNING)

    # Loại trùng lặp nhưng giữ thứ tự
    reasons = list(dict.fromkeys(reasons))
    warnings = list(dict.fromkeys(warnings))

    return {
        "signal": {
            "action": action,
            "confidence": score,
            "title": text["title"],
            "summary": text["summary"],
        },
        "reasons": reasons,
        "warnings": warnings,
    }


def build_suggested_order(signal_action, current_price, risk_management, levels, market):
    """Sinh lệnh gợi ý ưu tiên LO cho người mới."""
    entry = risk_management.get("entryZone", {}) or {}
    take_profit = risk_management.get("takeProfitZone", {}) or {}
    buy_price = entry.get("to") or entry.get("from")
    sell_price = None

    order_type = "LO"
    action = "WAIT_BUY"
    note = "Ưu tiên lệnh LO để kiểm soát giá. Không nên mua đuổi."

    if signal_action == "BUY":
        action = "BUY_LIMIT"
        note = "Có thể xem xét lệnh LO trong vùng mua tham khảo, luôn đặt stop loss và không dùng toàn bộ vốn."
    elif signal_action == "WATCH":
        action = "WAIT_BUY"
        note = "Chờ giá về vùng entry hoặc breakout rõ ràng kèm volume, không nên mua đuổi."
    elif signal_action == "HOLD":
        action = "HOLD"
        buy_price = None
        note = "Nếu đang có cổ phiếu có thể tiếp tục nắm giữ. Nếu chưa có thì nên theo dõi thêm, không mua vội."
    elif signal_action == "SELL":
        action = "SELL_LIMIT"
        buy_price = None
        sell_price = round_price_vn(current_price) or take_profit.get("from")
        note = "Cân nhắc bán LO hoặc giảm tỷ trọng. Không ưu tiên ATO/ATC cho người mới nếu chưa có kế hoạch rõ ràng."
    elif signal_action == "CUT_LOSS":
        action = "CUT_LOSS"
        buy_price = None
        sell_price = round_price_vn(current_price)
        note = "Ưu tiên bảo toàn vốn. Có thể đặt LO quanh giá hiện tại; nếu thủng hỗ trợ mạnh và cần thoát nhanh thì cân nhắc MP, nhưng MP có thể khớp giá xấu."

    return {
        "orderType": order_type,
        "action": action,
        "buyPrice": buy_price,
        "sellPrice": sell_price,
        "note": note,
    }


# ==========================================================
# API LẤY DỮ LIỆU VÀ PHÂN TÍCH CHỨNG KHOÁN
# ==========================================================

@app.route("/stock/<symbol>", methods=["GET"])
def get_stock_analysis(symbol):
    try:
        if not symbol or symbol.strip() == "":
            return jsonify({"error": "Mã cổ phiếu không được để trống"}), 400

        symbol_upper = symbol.strip().upper()
        stock_api = Vnstock().stock(symbol=symbol_upper, source="VCI")

        current_time = datetime.now()
        start_date = (current_time - timedelta(days=365 * 2)).strftime("%Y-%m-%d")
        end_date = current_time.strftime("%Y-%m-%d")

        raw_df = stock_api.quote.history(start=start_date, end=end_date, interval="1D")
        df = prepare_ohlcv_dataframe(raw_df, multiply_price_by_1000=True)

        if df is None or df.empty:
            return jsonify({"error": f"Không tìm thấy dữ liệu giao dịch cho mã: {symbol_upper}"}), 442

        if len(df) < 20:
            return jsonify({"error": f"Dữ liệu cho mã {symbol_upper} quá ít để phân tích kỹ thuật"}), 442

        # Lấy intraday/realtime nếu có. Không crash nếu vnstock lỗi intraday.
        realtime_price = None
        has_intraday = False
        try:
            intraday = stock_api.quote.intraday()
            if intraday is not None and not intraday.empty and "price" in intraday.columns:
                realtime_price = normalize_price_value(intraday.iloc[-1]["price"], True)
                has_intraday = realtime_price is not None
        except Exception:
            pass

        last_row_date = df.iloc[-1]["time"].date()
        today_date = current_time.date()

        if last_row_date == today_date and len(df) >= 2:
            previous_close = safe_float(df.iloc[-2]["close"])
            if realtime_price is None:
                realtime_price = safe_float(df.iloc[-1]["close"])
            else:
                # Cập nhật close hiện tại để chỉ báo gần realtime hơn.
                df.loc[df.index[-1], "close"] = realtime_price
                df.loc[df.index[-1], "high"] = max(safe_float(df.iloc[-1]["high"], realtime_price), realtime_price)
                df.loc[df.index[-1], "low"] = min(safe_float(df.iloc[-1]["low"], realtime_price), realtime_price)
        elif has_intraday:
            previous_close = safe_float(df.iloc[-1]["close"])
            # Không append dòng giả để tránh làm sai OHLCV; dùng giá realtime cho phân tích hiện tại.
        else:
            previous_close = safe_float(df.iloc[-1]["close"])
            realtime_price = previous_close

        if previous_close is None or previous_close == 0 or realtime_price is None:
            return jsonify({"error": f"Không đủ dữ liệu giá để phân tích mã {symbol_upper}"}), 442

        # Thêm chỉ báo sau khi đã cập nhật close nếu có dữ liệu intraday cùng ngày.
        df = add_technical_indicators(df)
        latest = df.iloc[-1]

        current_price = safe_float(realtime_price)
        price_change = current_price - previous_close
        percent_change = (price_change / previous_close) * 100 if previous_close else 0

        if price_change > 0:
            status, color = "up", "green"
        elif price_change < 0:
            status, color = "down", "red"
        else:
            status, color = "unchanged", "yellow"

        technical = {
            "rsi14": round_number(latest.get("RSI"), 2),
            "ma20": round_price_vn(latest.get("MA20")),
            "ma50": round_price_vn(latest.get("MA50")),
            "ma100": round_price_vn(latest.get("MA100")),
            "ma200": round_price_vn(latest.get("MA200")),
            "macd": round_number(latest.get("MACD"), 2),
            "macdSignal": round_number(latest.get("Signal_Line"), 2),
            "macdHistogram": round_number(latest.get("MACD_Histogram"), 2),
            "volume": round_number(latest.get("volume"), 0),
            "avgVolume20": round_number(latest.get("avgVolume20"), 0),
            "bollingerUpper": round_price_vn(latest.get("Bollinger_Upper")),
            "bollingerLower": round_price_vn(latest.get("Bollinger_Lower")),
        }

        levels = find_support_resistance(df, current_price, lookback=120)
        risk_management = calculate_risk_management(current_price, technical, levels)
        market = analyze_vnindex_market()
        signal_result = analyze_signal(current_price, technical, levels, risk_management, market, df)
        suggested_order = build_suggested_order(
            signal_result["signal"]["action"], current_price, risk_management, levels, market
        )

        # Cảnh báo nếu MA200 chỉ là fallback do chưa đủ 200 phiên.
        warnings = signal_result["warnings"][:]
        if len(df) < 200:
            warnings.append("Dữ liệu chưa đủ 200 phiên nên MA200 chỉ mang tính tham khảo theo dữ liệu hiện có")
        if market.get("warning"):
            warnings.append(market.get("warning"))
        warnings = list(dict.fromkeys(warnings))

        # Chuẩn hóa dữ liệu chart 120 phiên gần nhất.
        chart_df = df.tail(120).copy()
        chart_df["time"] = chart_df["time"].dt.strftime("%Y-%m-%d")
        chart_cols = [
            "time", "open", "high", "low", "close", "volume",
            "MA20", "MA50", "MA100", "MA200", "RSI",
            "MACD", "Signal_Line", "MACD_Histogram",
            "Bollinger_Upper", "Bollinger_Lower", "avgVolume20",
        ]
        chart_df = chart_df[chart_cols].replace({np.nan: None})
        chart_data = chart_df.to_dict(orient="records")

        latest_time = latest["time"].strftime("%Y-%m-%d") if hasattr(latest["time"], "strftime") else str(latest["time"])

        response = {
            "symbol": symbol_upper,

            # Giữ field cũ để frontend cũ không lỗi
            "currentPrice": round_price_vn(current_price),
            "referencePrice": round_price_vn(previous_close),
            "previousClose": round_price_vn(previous_close),
            "priceChange": round_number(price_change, 2),
            "percentChange": round_number(percent_change, 2),
            "status": status,
            "color": color,
            "rsi": technical["rsi14"],
            "ma20": technical["ma20"],
            "data": chart_data,

            # Bổ sung snake_case nếu frontend/backend khác cần dùng
            "current_price": round_price_vn(current_price),
            "reference_price": round_price_vn(previous_close),
            "previous_close": round_price_vn(previous_close),
            "price_change": round_number(price_change, 2),
            "price_change_percent": round_number(percent_change, 2),

            # Giá cơ bản phiên mới nhất
            "open": round_price_vn(latest.get("open")),
            "high": round_price_vn(latest.get("high")),
            "low": round_price_vn(latest.get("low")),
            "close": round_price_vn(latest.get("close")),
            "volume": round_number(latest.get("volume"), 0),
            "time": latest_time,

            "technical": technical,
            "levels": levels,
            "riskManagement": risk_management,
            "market": market,
            "signal": signal_result["signal"],
            "suggestedOrder": suggested_order,
            "reasons": signal_result["reasons"],
            "warnings": warnings,
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": f"Lỗi hệ thống Máy chủ Backend: {str(e)}"}), 500


# ==========================================================
# API XUẤT FILE BÁO CÁO EXCEL - GIỮ CHỨC NĂNG CŨ
# ==========================================================

@app.route("/export/<symbol>/<start_date>/<end_date>", methods=["GET"])
def export_excel(symbol, start_date, end_date):
    try:
        if not symbol or symbol.strip() == "":
            return jsonify({"error": "Mã cổ phiếu không được để trống"}), 400

        symbol_upper = symbol.strip().upper()

        try:
            start_obj = datetime.strptime(start_date, "%Y-%m-%d")
            end_obj = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            return jsonify({"error": "Định dạng ngày không hợp lệ. Vui lòng dùng YYYY-MM-DD"}), 400

        if start_obj > end_obj:
            return jsonify({"error": "Ngày bắt đầu không được lớn hơn ngày kết thúc"}), 400

        if start_obj > datetime.now() or end_obj > datetime.now():
            return jsonify({"error": "Hệ thống không hỗ trợ trích xuất dữ liệu ngày tương lai"}), 400

        stock_api = Vnstock().stock(symbol=symbol_upper, source="VCI")
        df = stock_api.quote.history(start=start_date, end=end_date, interval="1D")
        df = prepare_ohlcv_dataframe(df, multiply_price_by_1000=True)

        if df is None or df.empty:
            return jsonify({"error": f"Không có dữ liệu lịch sử để xuất file cho mã {symbol_upper}"}), 442

        df["Change"] = df["close"].diff().fillna(0)
        df["PercentChange"] = (df["close"].pct_change() * 100).fillna(0)
        df = df[df["time"] >= pd.to_datetime(start_date)].reset_index(drop=True)

        wb = Workbook()
        ws = wb.active
        ws.title = symbol_upper

        normal_font = Font(name="Arial", size=8)
        header_font = Font(name="Arial", size=8, color="FFFFFF", bold=True)
        blue_fill = PatternFill(start_color="0066CC", end_color="0066CC", fill_type="solid")
        center = Alignment(horizontal="center", vertical="center")

        inline_bold = InlineFont(rFont="Arial", sz=8, b=True)
        inline_normal = InlineFont(rFont="Arial", sz=8, b=False)
        inline_link = InlineFont(rFont="Arial", sz=8, b=False, u="single", color=Color(rgb="0000FF"))

        ws["A1"] = CellRichText([TextBlock(inline_bold, "Email: "), TextBlock(inline_normal, DEVELOPER_EMAIL)])
        ws["A2"] = CellRichText([TextBlock(inline_bold, "Phone: "), TextBlock(inline_normal, DEVELOPER_PHONE)])

        ws["A3"] = CellRichText([TextBlock(inline_bold, "GitHub: "), TextBlock(inline_link, "Tại đây")])
        ws["A3"].hyperlink = DEVELOPER_GITHUB
        ws["A3"].style = "Hyperlink"

        ws["A4"] = CellRichText([TextBlock(inline_bold, "Web: "), TextBlock(inline_link, "Tại đây")])
        ws["A4"].hyperlink = DEVELOPER_WEB
        ws["A4"].style = "Hyperlink"

        headers = [
            "NGÀY", "GIÁ MỞ CỬA", "GIÁ CAO NHẤT", "GIÁ THẤP NHẤT",
            "GIÁ ĐÓNG CỬA", "THAY ĐỔI GIÁ", "% THAY ĐỔI", "KHỐI LƯỢNG",
        ]
        header_row = 5

        for col_num, header in enumerate(headers, 1):
            cell = ws.cell(row=header_row, column=col_num)
            cell.value = header
            cell.fill = blue_fill
            cell.font = header_font
            cell.alignment = center

        data_start_row = 6
        for row_num, (_, row) in enumerate(df.iterrows(), data_start_row):
            values = [
                row["time"].strftime("%d/%m/%Y"),
                float(row["open"]), float(row["high"]), float(row["low"]), float(row["close"]),
                float(row["Change"]), float(row["PercentChange"]), float(row["volume"]),
            ]

            for col_num, value in enumerate(values, 1):
                cell = ws.cell(row=row_num, column=col_num, value=value)
                cell.font = normal_font
                cell.alignment = center

                if col_num in [2, 3, 4, 5, 6]:
                    cell.number_format = "#,##0.00"
                elif col_num == 7:
                    cell.number_format = "0.00"
                elif col_num == 8:
                    cell.number_format = "#,##0"

        for column in ws.columns:
            max_length = 0
            column_letter = get_column_letter(column[0].column)
            for cell in column:
                try:
                    if cell.value and not isinstance(cell.value, CellRichText):
                        max_length = max(max_length, len(str(cell.value)))
                except Exception:
                    pass
            ws.column_dimensions[column_letter].width = max_length + 5

        ws.column_dimensions["A"].width = 14

        excel_file = BytesIO()
        wb.save(excel_file)
        excel_file.seek(0)

        response = send_file(
            excel_file,
            download_name=f"{symbol_upper}_{start_date}_{end_date}.xlsx",
            as_attachment=True,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response.headers["Access-Control-Expose-Headers"] = "Content-Disposition"
        return response

    except Exception as e:
        return jsonify({"error": f"Lỗi xuất tệp Excel hệ thống: {str(e)}"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
