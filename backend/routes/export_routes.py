from flask import Blueprint, jsonify, send_file

from extensions import limiter
from services.export_service import EXCEL_MIME_TYPE, create_excel_report


export_bp = Blueprint("export", __name__)


@export_bp.route("/export/<symbol>/<start_date>/<end_date>", methods=["GET"])
@limiter.limit("10 per minute")
def export_excel(symbol, start_date, end_date):
    excel_file, filename, error, status_code = create_excel_report(symbol, start_date, end_date)

    if error is not None:
        return jsonify(error), status_code

    response = send_file(
        excel_file,
        download_name=filename,
        as_attachment=True,
        mimetype=EXCEL_MIME_TYPE,
        max_age=0,
    )
    response.headers["Access-Control-Expose-Headers"] = "Content-Disposition"
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    return response
