
from flask import jsonify

from . import accounts_bp
from ..services.account_service import AccountService


@accounts_bp.route("/rest/user/register", methods=["POST"])
def register_player():
    try:
        result = AccountService.create_player()

        return jsonify({
            "success": True,
            "id": result["player_id"],
            "userId": result["player_id"],
            "type": "anonymous"
        }), 201

    except Exception:
        return jsonify({
            "success": False,
            "error": "Registration failed"
        }), 500


@accounts_bp.route("/rest/user/<player_id>", methods=["GET"])
def get_player(player_id):
    try:
        player = AccountService.get_player(player_id)

        if player is None:
            return jsonify({
                "success": False,
                "error": "Player not found"
            }), 404

        return jsonify({
            "success": True,
            "player": player
        }), 200

    except Exception:
        return jsonify({
            "success": False,
            "error": "Database error"
        }), 500
