from flask import Blueprint

inventory = Blueprint('inventario', __name__)

from inventario.Infrastructure import routes