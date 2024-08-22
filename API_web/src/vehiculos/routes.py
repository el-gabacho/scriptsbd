from flask import jsonify, request
from sqlalchemy.exc import ProgrammingError
from vehiculos.funciones import get_marcas, get_buscar_marcas_similar, \
    obtener_modelos, get_buscar_modelos_similar
from vehiculos import vehicles as routes

# -----------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------
# CONSULTA PRINCIPAL DE VEHICULOS : MARCAS

@routes.route('/marcas', methods=['GET'])
def get_marcas_with_model_count():
    try:
        marcas = get_marcas()
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


# -----------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------
# CONSULTA SECUNDARIA DE VEHICULOS : MARCAS (ID) : MODELOS

@routes.route('/marcas/<int:id>/modelos', methods=['GET'])
def get_models(id):
    try:
        modelo = obtener_modelos(id)
        return jsonify(modelo)
    except ProgrammingError as e:
        return jsonify({'error': 'Error en la estructura de la base de datos', 'details': str(e)}), 500
    except Exception as e:
        print(e)
        return jsonify({'error': 'Ocurrió un error inesperado', 'details': str(e)}), 500

# -----------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------
# CRUD DE MODELO: BUSCAR POR NOMBRE DEL MODELO, CREAR NUEVO MODELO, EDITAR MODELO Y ELIMINAR MODELO

@routes.route('/buscar_modelo_similar/<int:id>/<string:nombremodelo>', methods=['GET'])
def search_modelo_similar(id, nombremodelo):
    try:
        modelo = get_buscar_modelos_similar(id, nombremodelo)
        
        # Devuelve una lista vacía si no se encuentran productos similares
        if modelo is None or len(modelo) == 0:
            return jsonify([])
        
        # Devuelve la lista de productos similares
        return jsonify(modelo)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500