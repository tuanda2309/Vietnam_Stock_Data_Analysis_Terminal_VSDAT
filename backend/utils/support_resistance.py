from utils.helpers import safe_float, round_number, round_price_vn


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
