from flask import request, jsonify
from categorias.funciones import obtener_categorias, crear_categoria, eliminar_categoria, actualizar_categoria
from categorias import categories

@categories.route('/categorias', methods=['GET'])
def get_categorias():
    try:
        categorias = obtener_categorias()
        return jsonify(categorias)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@categories.route('/categorias', methods=['POST'])
def create_categoria():
    try:
        data = request.get_json()
        nombre = data.get('nombre')
        id_categoria = crear_categoria(nombre)
        return jsonify({'idCategoria': id_categoria}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@categories.route('/categorias/<int:id>', methods=['DELETE'])
def delete_categoria(id):
    try:
        eliminar_categoria(id)
        return jsonify({'message': 'Categoría eliminada correctamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@categories.route('/categorias/<int:id>', methods=['PUT'])
def update_categoria(id):
    try:
        data = request.get_json()
        nombre = data.get('nombre')
        actualizar_categoria(id, nombre)
        return jsonify({'message': 'Categoría actualizada correctamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500