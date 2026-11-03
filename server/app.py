
from flask import Flask, jsonify

from server.config import Config
from server.database import initialize_database

from server.routes import (
    health_bp,
    accounts_bp,
    sessions_bp,
    gamestate_bp
)


def create_app():
    app = Flask(__name__)

    app.config["MAX_CONTENT_LENGTH"] = Config.MAX_GAMESTATE_SIZE

    # Initialize database
    initialize_database()

    # Register API routes
    app.register_blueprint(health_bp)
    app.register_blueprint(accounts_bp)
    app.register_blueprint(sessions_bp)
    app.register_blueprint(gamestate_bp)

    @app.route("/", methods=["GET"])
    def index():
        return jsonify({
            "name": Config.PROJECT_NAME,
            "version": Config.SERVER_VERSION,
            "status": "online",
            "message": "Welcome to MinionsParadiseBrazil!"
        })

    @app.route("/config", methods=["GET"])
    def server_config():
        return jsonify({
            "project": Config.PROJECT_NAME,
            "version": Config.SERVER_VERSION,
            "protocol_status": "experimental",
            "features": {
                "accounts": True,
                "sessions": True,
                "gamestate": True
            }
        })

    return app


app = create_app()


if __name__ == "__main__":
    from waitress import serve

    print("======================================")
    print("      MINIONS PARADISE BRAZIL")
    print("======================================")
    print("Version:", Config.SERVER_VERSION)
    print("Port:", Config.PORT)
    print("Starting server...")

    serve(
        app,
        host=Config.HOST,
        port=Config.PORT,
        threads=4
    )
