from flask import Blueprint

categories = Blueprint('categorias', __name__)

from categorias import routes