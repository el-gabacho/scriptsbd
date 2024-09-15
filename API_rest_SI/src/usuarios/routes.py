from flask import request, jsonify
from usuarios.funciones import obtener_usuarios, obtener_usuario, crear_usuario, eliminar_usuario, actualizar_usuario
from usuarios import users as routes

@routes.route('/usuarios', methods=['GET'])
def get_usuarios():
    try:
        usuarios = obtener_usuarios()
        return jsonify(usuarios)
    except Exception as e:
        return jsonify({'error': 'Ocurrió un problema al obtener los usuarios. Por favor, inténtalo más tarde.'}), 500
    
@routes.route('/usuarios/<int:id>', methods=['GET'])
def get_usuario(id):
    try:
        usuario = obtener_usuario(id)
        if usuario:
            return jsonify(usuario)
        return jsonify({'error': 'Usuario no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': 'Ocurrió un problema al obtener el usuario. Por favor, inténtalo más tarde.'}), 500

@routes.route('/usuarios', methods=['POST'])
def create_usuario():
    try:
        data = request.get_json()
        nombre = data.get('nombreCompleto')
        usuario = data.get('nombreUsuario')
        contrasena = data.get('contrasena')
        idRol = data.get('idRol')
        
        if not nombre or nombre.strip() == '':
            return jsonify({'error': 'El nombre para crear el usuario es obligatorio.'}), 400
        if not usuario or usuario.strip() == '':
            return jsonify({'error': 'El nombre de usuario para crear el usuario es obligatorio.'}), 400
        if not contrasena or contrasena.strip() == '':
            return jsonify({'error': 'La contraseña para crear el usuario es obligatoria.'}), 400
        if not idRol:
            return jsonify({'error': 'El rol para crear el usuario es obligatorio.'}), 400
        
        id_usuario = crear_usuario(nombre, usuario, contrasena, idRol)
        return jsonify({'idUsuario': id_usuario}), 201
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'error': 'Hubo un problema al crear el usuario. Verifica su servidor y notifique al administrador.'}), 500


@routes.route('/usuarios/<int:id>', methods=['DELETE'])
def delete_usuario(id):
    try:
        eliminar_usuario(id)
        return jsonify({'message': 'Usuario eliminado correctamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@routes.route('/usuarios/<int:id>', methods=['PUT'])
def update_usuario(id):
    try:
        data = request.get_json()
        nombre = data.get('nombreCompleto')
        usuario = data.get('nombreUsuario')
        contrasena = data.get('contrasena')
        idRol = data.get('idRol')
        fecha = data.get('fechaCreacion')
        
        if not nombre or nombre.strip() == '':
            return jsonify({'error': 'El nombre para editar el usuario es obligatorio.'}), 400
        if not usuario or usuario.strip() == '':
            return jsonify({'error': 'El nombre de usuario para editar el usuario es obligatorio.'}), 400
        if not contrasena or contrasena.strip() == '':
            return jsonify({'error': 'La contraseña para editar el usuario es obligatoria.'}), 400
        if not idRol:
            return jsonify({'error': 'El rol para editar el usuario es obligatorio.'}), 400
        
        resultado = actualizar_usuario(id, nombre, usuario, contrasena, idRol, fecha)
        if resultado == 'sin_cambio':
            return jsonify({'error': 'El usuario ya tenía los datos proporcionados. No se realizaron cambios.'}), 400
        elif resultado:
            return jsonify({'message': 'Usuario actualizado correctamente'}), 200
            
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'error': 'Hubo un problema al actualizar el usuario. Verifica su servidor y notifique al administrador.'}), 500