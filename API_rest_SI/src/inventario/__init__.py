from flask import Blueprint

inventory = Blueprint('inventario', __name__)

from inventario import routes