import os

from flask import Flask
from flask_cors import CORS

from routes.stock_routes import stock_bp
from routes.export_routes import export_bp


def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
    app.register_blueprint(stock_bp)
    app.register_blueprint(export_bp)
    return app


app = create_app()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
