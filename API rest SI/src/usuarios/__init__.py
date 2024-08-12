from flask import Blueprint

users = Blueprint('usuarios', __name__)

from usuarios.Infrastructure import routes