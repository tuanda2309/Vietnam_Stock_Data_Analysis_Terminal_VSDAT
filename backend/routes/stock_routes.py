from flask import Blueprint, jsonify

from extensions import limiter
from services.stock_service import get_stock_analysis_data


stock_bp = Blueprint("stock", __name__)


@stock_bp.route("/stock/<symbol>", methods=["GET"])
@limiter.limit("30 per minute")
def get_stock_analysis(symbol):
    data, status_code = get_stock_analysis_data(symbol)
    return jsonify(data), status_code
