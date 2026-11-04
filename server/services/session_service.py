
from datetime import datetime, timedelta, timezone

from ..config import Config
from ..database import get_connection
from ..security import (
    generate_session_id,
    generate_session_key,
    hash_session_key,
    verify_session_key
)


class SessionService:

    @staticmethod
    def create_session(player_id):
        if not isinstance(player_id, str) or not player_id:
            return None

        session_id = generate_session_id()
        session_key = generate_session_key()
        expires_at = (
            datetime.now(timezone.utc)
            + timedelta(hours=Config.SESSION_DURATION_HOURS)
        ).isoformat()

        with get_connection() as connection:
            player = connection.execute(
                "SELECT player_id FROM players WHERE player_id = ?",
                (player_id,)
            ).fetchone()

            if not player:
                return None

            connection.execute(
                """
                INSERT INTO sessions
                (session_id, player_id, session_key_hash, expires_at)
                VALUES (?, ?, ?, ?)
                """,
                (
                    session_id,
                    player_id,
                    hash_session_key(session_key),
                    expires_at
                )
            )
            connection.commit()

        return {
            "session_id": session_id,
            "player_id": player_id,
            "session_key": session_key,
            "expires_at": expires_at
        }

    @staticmethod
    def validate_session(player_id, session_key):
        if not isinstance(player_id, str) or not isinstance(session_key, str):
            return False

        with get_connection() as connection:
            sessions = connection.execute(
                """
                SELECT session_key_hash, expires_at
                FROM sessions
                WHERE player_id = ?
                """,
                (player_id,)
            ).fetchall()

            now = datetime.now(timezone.utc)

            for session in sessions:
                try:
                    expiration = datetime.fromisoformat(
                        session["expires_at"]
                    )

                    if expiration.tzinfo is None:
                        expiration = expiration.replace(
                            tzinfo=timezone.utc
                        )

                    if expiration <= now:
                        continue

                    if verify_session_key(
                        session_key,
                        session["session_key_hash"]
                    ):
                        return True

                except (ValueError, TypeError):
                    continue

        return False
