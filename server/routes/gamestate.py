
from flask import jsonify, request

from . import gamestate_bp
from ..services.gamestate_service import GameStateService
from ..services.session_service import SessionService


def authenticate_request():
    player_id = request.headers.get("User-Id")
    session_key = request.headers.get("Session-Key")

    if not player_id or not session_key:
        return None

    if not SessionService.validate_session(player_id, session_key):
        return None

    return player_id


@gamestate_bp.route("/rest/gamestate/<player_id>", methods=["GET"])
def get_gamestate(player_id):
    authenticated_id = authenticate_request()

    if authenticated_id != player_id:
        return jsonify({
            "success": False,
            "error": "Unauthorized"
        }), 401

    try:
        result = GameStateService.get_state(player_id)

        if result is None:
            return jsonify({
                "success": False,
                "error": "GameState not found"
            }), 404

        return jsonify({
            "success": True,
            "playerId": player_id,
            "gameState": result["state"],
            "updatedAt": result["updated_at"]
        }), 200

    except Exception:
        return jsonify({
            "success": False,
            "error": "GameState retrieval failed"
        }), 500


@gamestate_bp.route("/rest/gamestate/<player_id>", methods=["POST"])
def save_gamestate(player_id):
    authenticated_id = authenticate_request()

    if authenticated_id != player_id:
        return jsonify({
            "success": False,
            "error": "Unauthorized"
        }), 401

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "success": False,
            "error": "Invalid JSON object"
        }), 400

    try:
        saved = GameStateService.save_state(player_id, data)

        if not saved:
            return jsonify({
                "success": False,
                "error": "Player not found"
            }), 404

        return jsonify({
            "success": True,
            "message": "GameState saved"
        }), 200

    except ValueError as error:
        return jsonify({
            "success": False,
            "error": str(error)
        }), 400

    except Exception:
        return jsonify({
            "success": False,
            "error": "GameState save failed"
        }), 500
