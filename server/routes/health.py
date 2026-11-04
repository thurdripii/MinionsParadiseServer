
from flask import jsonify

from . import health_bp
from ..database import get_connection


@health_bp.route("/health", methods=["GET"])
def health():
    try:
        with get_connection() as connection:
            connection.execute("SELECT 1").fetchone()

        return jsonify({
            "status": "ok",
            "database": "connected"
        }), 200

    except Exception:
        return jsonify({
            "status": "error",
            "database": "unavailable"
        }), 503
