from flask import Flask
from config import configuracion
from models import db, ma  # Importar db y ma para inicializarlos
import routes

app = Flask(__name__)
app.config.from_object(configuracion['development'])

# Inicializar la base de datos y Marshmallow
db.init_app(app)
ma.init_app(app)

#prueba de cambio 
# Registrar las rutas desde el Blueprint
app.register_blueprint(routes.routes)

if __name__ == '__main__':
    app.run(debug=True)
