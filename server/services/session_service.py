
from datetime import datetime, timedelta, timezone

from ..config import Config
from ..database import get_connection
from ..security import (
    generate_session_id,
    generate_session_key,
    hash_session_key
)


class SessionService:

    @staticmethod
    def create_session(player_id):
        connection = get_connection()

        try:
            player = connection.execute(
                "SELECT player_id FROM players WHERE player_id = ?",
                (player_id,)
            ).fetchone()

            if player is None:
                return None

            session_id = generate_session_id()
            session_key = generate_session_key()
            key_hash = hash_session_key(session_key)

            expires_at = (
                datetime.now(timezone.utc)
                + timedelta(hours=Config.SESSION_DURATION_HOURS)
            ).isoformat()

            connection.execute(
                """
                INSERT INTO sessions
                (session_id, player_id, session_key_hash, expires_at)
                VALUES (?, ?, ?, ?)
                """,
                (session_id, player_id, key_hash, expires_at)
            )

            connection.commit()

            return {
                "session_id": session_id,
                "session_key": session_key,
                "expires_at": expires_at
            }

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()

    @staticmethod
    def validate_session(player_id, session_key):
        if not session_key:
            return False

        key_hash = hash_session_key(session_key)
        connection = get_connection()

        try:
            session = connection.execute(
                """
                SELECT expires_at FROM sessions
                WHERE player_id = ? AND session_key_hash = ?
                """,
                (player_id, key_hash)
            ).fetchone()

            if session is None:
                return False

            expiration = datetime.fromisoformat(
                session["expires_at"]
            )

            if expiration <= datetime.now(timezone.utc):
                connection.execute(
                    """
                    DELETE FROM sessions
                    WHERE player_id = ? AND session_key_hash = ?
                    """,
                    (player_id, key_hash)
                )
                connection.commit()
                return False

            return True

        finally:
            connection.close()
