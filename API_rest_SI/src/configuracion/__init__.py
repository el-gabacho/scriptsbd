from flask import Blueprint

config = Blueprint('configuracion', __name__)

from configuracion.Infrastructure import routes