
import json

from ..config import Config
from ..database import get_connection


class GameStateService:

    @staticmethod
    def get_state(player_id):
        with get_connection() as connection:
            result = connection.execute(
                """
                SELECT state_json, version, updated_at
                FROM gamestates
                WHERE player_id = ?
                """,
                (player_id,)
            ).fetchone()

            if not result:
                return None

            try:
                state = json.loads(result["state_json"])
            except (ValueError, TypeError):
                return None

            return {
                "player_id": player_id,
                "state": state,
                "version": result["version"],
                "updated_at": result["updated_at"]
            }

    @staticmethod
    def save_state(player_id, state):
        if not isinstance(player_id, str) or not player_id:
            return {"success": False, "error": "invalid_player_id"}

        try:
            state_json = json.dumps(
                state,
                ensure_ascii=False,
                separators=(",", ":")
            )
        except (TypeError, ValueError):
            return {"success": False, "error": "invalid_state"}

        if len(state_json.encode("utf-8")) > Config.MAX_GAMESTATE_SIZE:
            return {"success": False, "error": "state_too_large"}

        with get_connection() as connection:
            player = connection.execute(
                "SELECT player_id FROM players WHERE player_id = ?",
                (player_id,)
            ).fetchone()

            if not player:
                return {"success": False, "error": "player_not_found"}

            connection.execute(
                """
                INSERT INTO gamestates (player_id, state_json, version)
                VALUES (?, ?, 1)
                ON CONFLICT(player_id) DO UPDATE SET
                    state_json = excluded.state_json,
                    version = gamestates.version + 1,
                    updated_at = CURRENT_TIMESTAMP
                """,
                (player_id, state_json)
            )
            connection.commit()

        return {"success": True}

    @staticmethod
    def delete_state(player_id):
        with get_connection() as connection:
            cursor = connection.execute(
                "DELETE FROM gamestates WHERE player_id = ?",
                (player_id,)
            )
            connection.commit()
            return cursor.rowcount > 0
