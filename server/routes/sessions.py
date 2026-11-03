
from flask import jsonify, request

from . import sessions_bp
from ..services.session_service import SessionService


@sessions_bp.route("/rest/user/session", methods=["POST"])
def create_session():
    data = request.get_json(silent=True) or {}

    player_id = data.get("userId")

    if not isinstance(player_id, str) or not player_id:
        return jsonify({
            "success": False,
            "error": "Missing userId"
        }), 400

    try:
        session = SessionService.create_session(player_id)

        if session is None:
            return jsonify({
                "success": False,
                "error": "Player not found"
            }), 404

        return jsonify({
            "success": True,
            "sessionId": session["session_id"],
            "sessionKey": session["session_key"],
            "expiresAt": session["expires_at"]
        }), 200

    except Exception:
        return jsonify({
            "success": False,
            "error": "Session creation failed"
        }), 500


@sessions_bp.route("/rest/user/session/validate", methods=["POST"])
def validate_session():
    data = request.get_json(silent=True) or {}

    player_id = data.get("userId")
    session_key = data.get("sessionKey")

    if not isinstance(player_id, str) or not isinstance(session_key, str):
        return jsonify({
            "success": False,
            "error": "Missing credentials"
        }), 400

    try:
        valid = SessionService.validate_session(
            player_id,
            session_key
        )

        return jsonify({
            "success": valid
        }), 200 if valid else 401

    except Exception:
        return jsonify({
            "success": False,
            "error": "Session validation failed"
        }), 500
