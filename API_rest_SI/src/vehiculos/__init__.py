from flask import Blueprint

vehicles = Blueprint('vehiculos', __name__)

from vehiculos.Infrastructure import routes