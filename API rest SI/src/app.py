from flask import Flask
from config import configuracion
from init import db, ma  # Importar db y ma para inicializarlos
from auth import auth
from categorias import categories
from usuarios import users
from proveedores import suppliers
from ventas import sales
from vehiculos import vehicles
from inventario import inventory
from configuracion import config

#cambio
app = Flask(__name__)
app.config.from_object(configuracion['development'])

# Inicializar la base de datos y Marshmallow
db.init_app(app)
ma.init_app(app)

#prueba de cambio 
# Registrar las rutas desde el Blueprint
app.register_blueprint(auth)
app.register_blueprint(categories)
app.register_blueprint(users)
app.register_blueprint(suppliers)
app.register_blueprint(sales)
app.register_blueprint(vehicles)
app.register_blueprint(inventory)
app.register_blueprint(config)

if __name__ == '__main__':
    app.run(debug=True)
