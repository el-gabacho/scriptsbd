from usuarios.Domain.Usuario import Usuario
from flask import jsonify, make_response

def iniciar_sesion(username, password):
    sesion = {}
    
    user = Usuario.query.filter_by(usuario=username).first()
    
    if user is None or not user.check_password(password):
        return make_response(jsonify({'error': 'Invalid username or password'}), 401)
    
    if user.estado == False:
        return make_response(jsonify({'error': 'User is disabled'}), 403)
    
    sesion['id'] = user.idUsuario
    sesion['idRol'] = user.idRol
    sesion['usuario'] = user.usuario
    
    return sesion