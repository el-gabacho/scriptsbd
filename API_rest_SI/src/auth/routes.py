from . import auth
from flask import request, jsonify
from auth.funciones import iniciar_sesion

@auth.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('usuario')
        password = data.get('contrasena')
        
        if not username or not password:
            return jsonify({'error':'Faltan algunos datos para iniciar sesión. Asegúrate de ingresar tanto el usuario como la contraseña.'}), 400
        
        # Llamar a la función para autenticar el usuario
        sesion = iniciar_sesion(username, password)
        return sesion
    except Exception as e:
        print(e)
        return jsonify({'error':'Hubo un problema con el servidor. Por favor, inténtalo más tarde o contacta con el administrador si el problema persiste.'}), 500