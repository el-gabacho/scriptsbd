from flask import jsonify, request
from proveedores.Application.funciones import obtener_proveedores, obtener_proveedor, crear_proveedor, eliminar_proveedor, actualizar_proveedor
from proveedores import suppliers as routes

@routes.route('/proveedores', methods=['GET'])
def get_proveedores():
    try:
        proveedores = obtener_proveedores()
        return jsonify(proveedores)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@routes.route('/proveedores/<int:id>', methods=['GET'])
def get_proveedor(id):
    try:
        proveedor = obtener_proveedor(id)
        if proveedor:
            return jsonify(proveedor)
        return jsonify({'message': 'Proveedor no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@routes.route('/proveedores', methods=['POST'])
def crearte_proveedor():
    try:
        data = request.get_json()
        nombre = data.get('nombre')
        encargado = data.get('encargado')
        telefono = data.get('telefono')
        correo = data.get('correo')
        id_proveedor = crear_proveedor(nombre, encargado, telefono, correo)
        return jsonify({'idCategoria': id_proveedor}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@routes.route('/proveedores/<int:id>', methods=['DELETE'])
def delete_proveedor(id):
    try:
        eliminar_proveedor(id)
        return jsonify({'message': 'Proveedor eliminado correctamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@routes.route('/proveedores/<int:id>', methods=['PUT'])
def update_proveedor(id):
    try:
        data = request.get_json()
        nombre = data.get('nombre')
        encargado = data.get('encargado')
        telefono = data.get('telefono')
        correo = data.get('correo')
        response = actualizar_proveedor(id, nombre, encargado, telefono, correo)
        return jsonify({'message': 'Proveedor actualizado correctamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500