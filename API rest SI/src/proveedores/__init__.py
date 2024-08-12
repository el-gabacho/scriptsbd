from flask import Blueprint

suppliers = Blueprint('proveedores', __name__)

from proveedores.Infrastructure import routes