
import os
import sqlite3

from config import Config


def get_connection():
    database_dir = os.path.dirname(Config.DATABASE_PATH)

    os.makedirs(database_dir, exist_ok=True)

    connection = sqlite3.connect(
        Config.DATABASE_PATH,
        timeout=10
    )

    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def initialize_database():
    connection = get_connection()

    try:
        connection.executescript("""
            CREATE TABLE IF NOT EXISTS players (
                player_id TEXT PRIMARY KEY,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                player_id TEXT NOT NULL,
                session_key_hash TEXT NOT NULL UNIQUE,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                expires_at TEXT NOT NULL,

                FOREIGN KEY (player_id)
                    REFERENCES players(player_id)
                    ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS gamestates (
                player_id TEXT PRIMARY KEY,
                state_json TEXT NOT NULL,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (player_id)
                    REFERENCES players(player_id)
                    ON DELETE CASCADE
            );

            CREATE INDEX IF NOT EXISTS idx_sessions_player
            ON sessions(player_id);
        """)

        connection.commit()
        print("[MPB] Database initialized successfully.")

    except sqlite3.Error:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    initialize_database()
