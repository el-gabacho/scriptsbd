from flask import Blueprint

sales = Blueprint('ventas', __name__)

from ventas.Infrastructure import routes