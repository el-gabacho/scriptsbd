from flask import jsonify, request
from proveedores.funciones import obtener_proveedores, obtener_proveedor, crear_proveedor, eliminar_proveedor, actualizar_proveedor
from proveedores import suppliers as routes

@routes.route('/proveedores', methods=['GET'])
def get_proveedores():
    try:
        proveedores = obtener_proveedores()
        return jsonify(proveedores)
    except Exception as e:
        return jsonify({'error': 'Ocurrió un problema al obtener los proveedores. Por favor, inténtalo más tarde.'}), 500
    
    
@routes.route('/proveedores/<int:id>', methods=['GET'])
def get_proveedor(id):
    try:
        proveedor = obtener_proveedor(id)
        if proveedor:
            return jsonify(proveedor)
        return jsonify({'error': 'Proveedor no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': 'Ocurrió un problema al obtener el proveedor. Por favor, inténtalo más tarde.'}), 500
    

@routes.route('/proveedores', methods=['POST'])
def create_proveedor():
    try:
        data = request.get_json()
        nombre = data.get('nombre')
        encargado = data.get('encargado')
        telefono = data.get('telefono')
        correo = data.get('correo')
        
        if not nombre or nombre.strip() == '':
            return jsonify({'error': 'El nombre para crear el proveedor es obligatorio.'}), 400
        
        id_proveedor = crear_proveedor(nombre, encargado, telefono, correo)
        return jsonify({'idCategoria': id_proveedor}), 201
    
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'error': 'Hubo un problema al crear el proveedor. Verifica su servidor y notifique al administrador.'}), 500
    

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
        
        if not nombre or nombre.strip() == '':
            return jsonify({'error': 'El nombre para crear el proveedor es obligatorio.'}), 400
        
        resultado = actualizar_proveedor(id, nombre, encargado, telefono, correo)
        if resultado == 'sin_cambio':
            return jsonify({'error': 'El proveedor ya tenía la información proporcionada. No se realizaron cambios.'}), 400
        elif resultado:
            return jsonify({'message': 'Proveedor actualizado correctamente'}), 200
    
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'error': 'Hubo un problema al actualizar el proveedor. Verifica su servidor y notifique al administrador.'}), 500