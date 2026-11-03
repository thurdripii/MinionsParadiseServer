
import os

class Config:
    PROJECT_NAME = "MinionsParadiseBrazil"
    SERVER_VERSION = "0.2.0-dev"

    HOST = os.getenv("MP_HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))

    DATABASE_PATH = os.getenv(
        "MP_DATABASE_PATH",
        os.path.join(
            os.path.dirname(__file__),
            "data",
            "minions_paradise.db"
        )
    )

    DEBUG = os.getenv("MP_DEBUG", "false").lower() == "true"

    SESSION_DURATION_HOURS = 24
    MAX_GAMESTATE_SIZE = 1024 * 1024
