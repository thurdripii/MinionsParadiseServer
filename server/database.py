
import os
import sqlite3
from contextlib import contextmanager

from .config import Config


def ensure_database_directory():
    directory = os.path.dirname(Config.DATABASE_PATH)

    if directory:
        os.makedirs(directory, exist_ok=True)


@contextmanager
def get_connection():
    ensure_database_directory()

    connection = sqlite3.connect(
        Config.DATABASE_PATH,
        timeout=15
    )

    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("PRAGMA journal_mode = WAL")
    connection.execute("PRAGMA busy_timeout = 15000")

    try:
        yield connection
    finally:
        connection.close()


def initialize_database():
    ensure_database_directory()

    with get_connection() as connection:
        connection.executescript("""
            CREATE TABLE IF NOT EXISTS players (
                player_id TEXT PRIMARY KEY,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                player_id TEXT NOT NULL,
                session_key_hash TEXT NOT NULL UNIQUE,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                expires_at TEXT NOT NULL,

                FOREIGN KEY (player_id)
                    REFERENCES players(player_id)
                    ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS gamestates (
                player_id TEXT PRIMARY KEY,
                state_json TEXT NOT NULL,
                version INTEGER NOT NULL DEFAULT 1,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (player_id)
                    REFERENCES players(player_id)
                    ON DELETE CASCADE
            );

            CREATE INDEX IF NOT EXISTS idx_sessions_player
            ON sessions(player_id);

            CREATE INDEX IF NOT EXISTS idx_sessions_expiration
            ON sessions(expires_at);

            CREATE INDEX IF NOT EXISTS idx_players_created
            ON players(created_at);
        """)

        connection.commit()

    print("[MPB] Database initialized successfully.")


def check_database():
    try:
        with get_connection() as connection:
            result = connection.execute(
                "PRAGMA quick_check"
            ).fetchone()

            return result[0] == "ok"

    except sqlite3.Error as error:
        print("[MPB] Database check failed:", error)
        return False


if __name__ == "__main__":
    initialize_database()

    if check_database():
        print("[MPB] Database integrity: OK")
    else:
        print("[MPB] Database integrity: FAILED")
