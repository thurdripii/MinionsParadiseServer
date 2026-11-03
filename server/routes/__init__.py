
from flask import Blueprint

health_bp = Blueprint("health", __name__)
accounts_bp = Blueprint("accounts", __name__)
sessions_bp = Blueprint("sessions", __name__)
gamestate_bp = Blueprint("gamestate", __name__)
