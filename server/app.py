
import os
from flask import Flask, jsonify
from waitress import serve

app = Flask(__name__)

SERVER_NAME = "MinionsParadiseBrazil"
SERVER_VERSION = os.getenv("MP_SERVER_VERSION", "0.1.0-dev")
PORT = int(os.getenv("PORT", "8000"))


@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "name": SERVER_NAME,
        "version": SERVER_VERSION,
        "status": "online",
        "message": "Welcome to MinionsParadiseBrazil!"
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "server": SERVER_NAME,
        "version": SERVER_VERSION
    }), 200


@app.route("/config", methods=["GET"])
def config():
    return jsonify({
        "project": SERVER_NAME,
        "version": SERVER_VERSION,
        "protocol_status": "experimental",
        "features": {
            "diagnostics": True,
            "accounts": False,
            "sessions": False,
            "gamestate": False
        }
    }), 200


if __name__ == "__main__":
    print("======================================")
    print("      MINIONS PARADISE BRAZIL")
    print("======================================")
    print("Server version:", SERVER_VERSION)
    print("Port:", PORT)
    print("Starting server...")

    serve(app, host="0.0.0.0", port=PORT, threads=4)
