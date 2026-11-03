
from ..database import get_connection
from ..security import generate_player_id


class AccountService:

    @staticmethod
    def create_player():
        player_id = generate_player_id()

        with get_connection() as connection:
            connection.execute(
                "INSERT INTO players (player_id) VALUES (?)",
                (player_id,)
            )
            connection.commit()

        return {
            "success": True,
            "player_id": player_id
        }

    @staticmethod
    def get_player(player_id):
        with get_connection() as connection:
            player = connection.execute(
                """
                SELECT player_id, created_at, updated_at
                FROM players
                WHERE player_id = ?
                """,
                (player_id,)
            ).fetchone()

            return dict(player) if player else None
