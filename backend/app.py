import logging
import os

from flask import Flask, jsonify
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from extensions import limiter
from routes.stock_routes import stock_bp
from routes.export_routes import export_bp


DEFAULT_FRONTEND_URL = "https://vsdat-frontend.onrender.com"


def parse_allowed_origins():
    """Lấy danh sách domain frontend được phép gọi backend."""
    frontend_url = os.environ.get("FRONTEND_URL", DEFAULT_FRONTEND_URL)
    extra_origins = os.environ.get("CORS_EXTRA_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")
    raw_origins = f"{frontend_url},{extra_origins}"
    origins = []

    for origin in raw_origins.split(","):
        origin = origin.strip().rstrip("/")
        if origin and origin not in origins:
            origins.append(origin)

    return origins


def create_app():
    app = Flask(__name__)
    app.config["JSON_SORT_KEYS"] = False
    app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024

    logging.basicConfig(
        level=os.environ.get("LOG_LEVEL", "INFO"),
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )

    allowed_origins = parse_allowed_origins()
    CORS(
        app,
        resources={r"/*": {"origins": allowed_origins}},
        supports_credentials=False,
        expose_headers=["Content-Disposition"],
    )

    limiter.init_app(app)

    @app.get("/health")
    def health():
        return jsonify({"status": "ok", "service": "VSDAT backend"}), 200

    @app.after_request
    def add_security_headers(response):
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
        response.headers.setdefault("Cache-Control", "no-store")
        return response

    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        return jsonify({"error": error.description}), error.code

    @app.errorhandler(Exception)
    def handle_unexpected_exception(error):
        app.logger.exception("Unexpected backend error")
        return jsonify({"error": "Lỗi hệ thống máy chủ. Vui lòng thử lại sau."}), 500

    app.register_blueprint(stock_bp)
    app.register_blueprint(export_bp)

    return app


app = create_app()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
