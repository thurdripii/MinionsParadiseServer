
from flask import jsonify, request

from . import gamestate_bp
from ..services.session_service import SessionService
from ..services.gamestate_service import GameStateService


def authenticate(player_id):
    user_id = request.headers.get("User-Id")
    session_key = request.headers.get("Session-Key")

    if user_id != player_id or not session_key:
        return False

    return SessionService.validate_session(user_id, session_key)


@gamestate_bp.route("/rest/gamestate/<player_id>", methods=["GET"])
def get_gamestate(player_id):
    if not authenticate(player_id):
        return jsonify({
            "success": False,
            "error": "unauthorized"
        }), 401

    result = GameStateService.get_state(player_id)

    if result is None:
        return jsonify({
            "success": False,
            "error": "gamestate_not_found"
        }), 404

    return jsonify({
        "success": True,
        "data": result
    }), 200


@gamestate_bp.route("/rest/gamestate/<player_id>", methods=["POST"])
def save_gamestate(player_id):
    if not authenticate(player_id):
        return jsonify({
            "success": False,
            "error": "unauthorized"
        }), 401

    payload = request.get_json(silent=True)

    if not isinstance(payload, dict):
        return jsonify({
            "success": False,
            "error": "invalid_json"
        }), 400

    state = payload.get("data", payload)

    result = GameStateService.save_state(player_id, state)

    if not result["success"]:
        status = 404 if result["error"] == "player_not_found" else 400
        return jsonify(result), status

    return jsonify(result), 200
