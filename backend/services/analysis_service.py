from constants import RISK_WARNING
from utils.helpers import safe_float, round_price_vn


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
    # warnings.append(RISK_WARNING)

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
