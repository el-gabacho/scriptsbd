from usuarios.modelos import Usuario
from flask import jsonify, make_response

def iniciar_sesion(username, password):
    sesion = {}
    
    # Buscar el usuario en la base de datos
    user = Usuario.query.filter_by(usuario=username).first()
    
    # Verificar si el usuario no existe o si la contraseña es incorrecta
    if user is None or not user.check_password(password):
        return make_response(jsonify({'error': 'Credenciales incorrectas'}), 401)
    
    # Verificar si el usuario está deshabilitado
    if user.estado == 0:
        return make_response(jsonify({'error': 'El usuario está deshabilitado'}), 403)
    
    # Verificar si el usuario tiene un idRol no permitido (idRol == 3)
    if user.idRol == 3:
        return make_response(jsonify({'error': 'No tienes permisos para acceder a esta sección'}), 403)
    
    # Verificar si el idRol es 1 o 2 (roles permitidos)
    if user.idRol in [1, 2]:
        sesion['id'] = user.idUsuario
        sesion['idRol'] = user.idRol
        sesion['usuario'] = user.usuario
        return jsonify(sesion)