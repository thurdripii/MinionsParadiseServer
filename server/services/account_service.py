
from ..database import get_connection
from ..security import generate_player_id


class AccountService:

    @staticmethod
    def create_player():
        player_id = generate_player_id()
        connection = get_connection()

        try:
            connection.execute(
                "INSERT INTO players (player_id) VALUES (?)",
                (player_id,)
            )

            connection.commit()

            return {
                "success": True,
                "player_id": player_id
            }

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()

    @staticmethod
    def get_player(player_id):
        connection = get_connection()

        try:
            player = connection.execute(
                "SELECT player_id, created_at FROM players "
                "WHERE player_id = ?",
                (player_id,)
            ).fetchone()

            if player is None:
                return None

            return dict(player)

        finally:
            connection.close()
