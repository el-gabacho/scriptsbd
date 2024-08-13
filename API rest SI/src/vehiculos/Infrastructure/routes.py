from flask import jsonify, request
from sqlalchemy.exc import ProgrammingError
from vehiculos.Application.funciones import get_marcas_count_modelos, get_modelos_count_productos, \
    crear_marca, obtener_modelo_anio_con_count
from vehiculos import vehicles as routes

# -----------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------
# CONSULTA PRINCIPAL DE VEHICULOS : MARCAS

@routes.route('/marcas_numero_modelos', methods=['GET'])
def get_marcas_with_model_count():
    try:
        marcas = get_marcas_count_modelos()
        return jsonify(marcas)
    except ProgrammingError as e:
        return jsonify({'error': 'Error en la estructura de la base de datos', 'details': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Ocurrió un error inesperado', 'details': str(e)}), 500

# -----------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------
# CRUD DE MARCA: BUSCAR POR NOMBRE DE LA MARCA, CREAR NUEVA MARCA, EDITAR MARCA Y ELIMINAR MARCA

# CREAR UNA NUEVA MARCA
@routes.route('/nueva_marca', methods=['POST'])
def create_marca():
    data = request.get_json()
    nombre = data.get('nombre')
    urlLogo = data.get('urlLogo', None)  # Permitir None si no se proporciona

    if not nombre:
        return jsonify({'error': 'El nombre de la marca es obligatorio'}), 400

    marca, error = crear_marca(nombre, urlLogo)

    if error:
        return jsonify({'error': error}), 409

    return jsonify({'message': 'Marca creada exitosamente', 'idMarca': marca.idMarca}), 201





# -----------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------
# CONSULTA SECUNDARIA DE VEHICULOS : MARCAS (ID) : MODELOS

@routes.route('/modelos_numero_productos/<int:id>', methods=['GET'])
def get_modelos_with_productos_count(id):
    try:
        marca = get_modelos_count_productos(id)
        if marca:
            return jsonify(marca)
        return jsonify({'message': 'Marca no encontrada'}), 404
    except ProgrammingError as e:
        return jsonify({'error': 'Error en la estructura de la base de datos', 'details': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Ocurrió un error inesperado', 'details': str(e)}), 500

# -----------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------

@routes.route('/modelos/<int:idmarca>', methods=['GET'])
def get_modelo_anio_count(idmarca):
    try:
        modelos = obtener_modelo_anio_con_count(idmarca)
        return jsonify(modelos)
    except ProgrammingError as e:
        return jsonify({'error': 'Error en la estructura de la base de datos', 'details': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Ocurrió un error inesperado', 'details': str(e)}), 500