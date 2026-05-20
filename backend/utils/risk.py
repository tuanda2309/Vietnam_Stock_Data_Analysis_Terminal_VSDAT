from utils.helpers import safe_float, round_number, round_price_vn


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
