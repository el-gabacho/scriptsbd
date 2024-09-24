from usuarios.modelos import Usuario
from flask import jsonify

def iniciar_sesion(username, password):
    sesion = {}
    
    # Buscar el usuario en la base de datos
    user = Usuario.query.filter_by(usuario=username).first()
    
    # Verificar si el usuario no existe o si la contraseña es incorrecta
    if user is None or not user.check_password(password):
        return jsonify({'error':'Las credenciales que has ingresado no son correctas. Por favor, verifica tu nombre de usuario y contraseña e inténtalo de nuevo.'}), 401
    
    # Verificar si el usuario está deshabilitado
    if user.estado == 0:
        return jsonify({'error' : 'No tienes permisos para acceder a esta sección, tu cuenta está deshabilitada. Contacta con el administrador para más detalles.'}), 403
    
    # Verificar si el usuario tiene un idRol no permitido (idRol == 3)
    sesion['id'] = user.idUsuario
    sesion['idRol'] = user.idRol
    sesion['usuario'] = user.usuario
    return jsonify(sesion)