from flask import jsonify, request
from sqlalchemy.exc import ProgrammingError
from vehiculos.Application.funciones import get_marcas_count_modelos, get_modelos_count_productos, \
    crear_marca, editar_marca, eliminar_marca, get_buscar_marcas_similar
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
        print(e)
        return jsonify({'error': 'Error en la estructura de la base de datos', 'details': str(e)}), 500
    except Exception as e:
        print(e)
        return jsonify({'error': 'Ocurrió un error inesperado', 'details': str(e)}), 500

# -----------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------
# CRUD DE MARCA: BUSCAR POR NOMBRE DE LA MARCA, CREAR NUEVA MARCA, EDITAR MARCA Y ELIMINAR MARCA

# BUSCAR POR NOMBRE DE LA MARCA SIMILITUD
@routes.route('/buscar_marca_similar/<string:nombremarca>', methods=['GET'])
def search_marca_similar(nombremarca):
    try:
        marcas = get_buscar_marcas_similar(nombremarca)
        
        # Devuelve una lista vacía si no se encuentran productos similares
        if marcas is None or len(marcas) == 0:
            return jsonify([])
        
        # Devuelve la lista de productos similares
        return jsonify(marcas)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# CREAR UNA NUEVA MARCA
@routes.route('/nueva_marca', methods=['POST'])
def create_marca():
    try:
        data = request.get_json()
        nombre = data.get('Nombre')
        urlLogo = data.get('UrlLogo', None)

        marca = crear_marca(nombre, urlLogo)
        return jsonify({'Marca': marca}), 201
    except Exception as e:
        return jsonify({'error':str(e)}), 500

# EDITAR UNA MARCA
@routes.route('/editar_marca/<int:idMarca>', methods=['PUT'])
def update_marca(idMarca):
    try:
        data = request.get_json()
        nombre = data.get('Nombre')
        urlLogo = data.get('UrlLogo', None)  # Permitir None si no se proporciona
        editar_marca(idMarca, nombre, urlLogo)
        return jsonify({'message': 'Marca actualizada correctamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ELIMINAR UNA MARCA
@routes.route('/eliminar_marca/<int:idMarca>', methods=['DELETE'])
def delete_marca(idMarca):
    try:
        eliminar_marca(id)
        return jsonify({'message': 'Marca eliminada correctamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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
