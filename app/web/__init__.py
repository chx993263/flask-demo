from flask import Blueprint
from app.error import init_error_handlers

auth_bp = Blueprint('auth', __name__)
h5_game = Blueprint('games', __name__, url_prefix='/v1/games/')

init_error_handlers(auth_bp)
init_error_handlers(h5_game)

# 路由
from app.web import auth
from app.web import games
