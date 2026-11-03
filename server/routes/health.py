
from flask import jsonify

from . import health_bp
from ..config import Config
from ..database import get_connection


@health_bp.route("/health", methods=["GET"])
def health():
    database_status = "ok"

    try:
        connection = get_connection()
        connection.execute("SELECT 1")
        connection.close()
    except Exception:
        database_status = "error"

    status_code = 200 if database_status == "ok" else 503

    return jsonify({
        "status": "ok" if status_code == 200 else "error",
        "server": Config.PROJECT_NAME,
        "version": Config.SERVER_VERSION,
        "database": database_status
    }), status_code


@health_bp.route("/ready", methods=["GET"])
def ready():
    return jsonify({
        "ready": True,
        "server": Config.PROJECT_NAME,
        "version": Config.SERVER_VERSION
    }), 200
