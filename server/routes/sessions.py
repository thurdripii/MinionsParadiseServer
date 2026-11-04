
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
            "error": "missing_user_id"
        }), 400

    session = SessionService.create_session(player_id)

    if not session:
        return jsonify({
            "success": False,
            "error": "player_not_found"
        }), 404

    return jsonify({
        "success": True,
        "sessionId": session["session_id"],
        "userId": session["player_id"],
        "sessionKey": session["session_key"],
        "expiresAt": session["expires_at"]
    }), 200


@sessions_bp.route("/rest/user/session/validate", methods=["POST"])
def validate_session():
    data = request.get_json(silent=True) or {}

    player_id = data.get("userId")
    session_key = data.get("sessionKey")

    if not player_id or not session_key:
        return jsonify({
            "success": False,
            "error": "missing_credentials"
        }), 400

    valid = SessionService.validate_session(
        player_id,
        session_key
    )

    return jsonify({
        "success": valid
    }), 200 if valid else 401
