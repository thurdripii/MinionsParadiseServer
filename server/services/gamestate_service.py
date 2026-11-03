
import json

from ..config import Config
from ..database import get_connection


class GameStateService:

    @staticmethod
    def save_state(player_id, state):
        if not isinstance(state, dict):
            raise ValueError("GameState must be a JSON object")

        state_json = json.dumps(
            state,
            separators=(",", ":"),
            ensure_ascii=False
        )

        if len(state_json.encode("utf-8")) > Config.MAX_GAMESTATE_SIZE:
            raise ValueError("GameState exceeds maximum size")

        connection = get_connection()

        try:
            player = connection.execute(
                "SELECT player_id FROM players WHERE player_id = ?",
                (player_id,)
            ).fetchone()

            if player is None:
                return False

            existing = connection.execute(
                "SELECT player_id FROM gamestates WHERE player_id = ?",
                (player_id,)
            ).fetchone()

            if existing:
                connection.execute(
                    """
                    UPDATE gamestates
                    SET state_json = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE player_id = ?
                    """,
                    (state_json, player_id)
                )
            else:
                connection.execute(
                    """
                    INSERT INTO gamestates (player_id, state_json)
                    VALUES (?, ?)
                    """,
                    (player_id, state_json)
                )

            connection.commit()
            return True

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()

    @staticmethod
    def get_state(player_id):
        connection = get_connection()

        try:
            result = connection.execute(
                """
                SELECT state_json, updated_at
                FROM gamestates
                WHERE player_id = ?
                """,
                (player_id,)
            ).fetchone()

            if result is None:
                return None

            return {
                "state": json.loads(result["state_json"]),
                "updated_at": result["updated_at"]
            }

        finally:
            connection.close()
