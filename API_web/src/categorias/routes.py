from flask import request, jsonify
from categorias.funciones import obtener_categorias
from categorias import categories

@categories.route('/categorias', methods=['GET'])
def get_categorias():
    try:
        categorias = obtener_categorias()
        return jsonify(categorias)
    except Exception as e:
        return jsonify({'error': str(e)}), 500