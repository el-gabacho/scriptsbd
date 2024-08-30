from flask import request, jsonify
from usuarios.funciones import obtener_usuarios, obtener_usuario, crear_usuario, eliminar_usuario, actualizar_usuario
from usuarios import users as routes
from tools.decorators import token_required

@routes.route('/usuarios', methods=['GET'])
# @token_required
def get_usuarios():
    try:
        usuarios = obtener_usuarios()
        return jsonify(usuarios)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@routes.route('/usuarios/<int:id>', methods=['GET'])
def get_usuario(id):
    try:
        usuario = obtener_usuario(id)
        if usuario:
            return jsonify(usuario)
        return jsonify({'message': 'Usuario no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@routes.route('/usuarios', methods=['POST'])
def create_usuario():
    try:
        data = request.get_json()
        print(data)
        nombre = data.get('nombreCompleto')
        usuario = data.get('nombreUsuario')
        contrasena = data.get('contrasena')
        idRol = data.get('idRol')
        id_usuario = crear_usuario(nombre, usuario, contrasena, idRol)
        return jsonify({'idUsuario': id_usuario}), 201
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500

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
        
        actualizar_usuario(id, nombre, usuario, contrasena, idRol, fecha)
        return jsonify({'message': 'Usuario actualizado correctamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500