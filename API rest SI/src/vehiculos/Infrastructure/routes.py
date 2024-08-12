from flask import jsonify
from sqlalchemy.exc import ProgrammingError
from vehiculos.Application.funciones import get_marcas_con_count_modelos, obtener_marca, obtener_modelo_anio_con_count
from vehiculos import vehicles as routes

@routes.route('/marcas', methods=['GET'])
def get_marcas_with_model_count():
    try:
        marcas = get_marcas_con_count_modelos()
        return jsonify(marcas)
    except ProgrammingError as e:
        return jsonify({'error': 'Error en la estructura de la base de datos', 'details': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Ocurrió un error inesperado', 'details': str(e)}), 500

@routes.route('/marcas/<int:id>', methods=['GET'])
def get_marca(id):
    try:
        marca = obtener_marca(id)
        if marca:
            return jsonify(marca)
        return jsonify({'message': 'Marca no encontrada'}), 404
    except ProgrammingError as e:
        return jsonify({'error': 'Error en la estructura de la base de datos', 'details': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Ocurrió un error inesperado', 'details': str(e)}), 500

@routes.route('/modelos/<int:idmarca>', methods=['GET'])
def get_modelo_anio_count(idmarca):
    try:
        modelos = obtener_modelo_anio_con_count(idmarca)
        return jsonify(modelos)
    except ProgrammingError as e:
        return jsonify({'error': 'Error en la estructura de la base de datos', 'details': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Ocurrió un error inesperado', 'details': str(e)}), 500