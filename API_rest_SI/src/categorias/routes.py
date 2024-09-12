from flask import request, jsonify
from categorias.funciones import obtener_categorias, crear_categoria, eliminar_categoria, actualizar_categoria,\
    obtener_categorias_similares
from categorias import categories

# -----------------------------------------------------------------------------------------------------------------------

@categories.route('/categorias', methods=['GET'])
def get_categorias():
    try:
        categorias = obtener_categorias()

        return jsonify(categorias), 200

    except Exception as e:
        # Devuelve un mensaje genérico para el cliente y loguea el detalle
        return jsonify({'Error': 'Ocurrió un problema al obtener las categorías. Por favor, inténtalo más tarde.'}), 500

# -----------------------------------------------------------------------------------------------------------------------

@categories.route('/categorias', methods=['POST'])
def create_categoria():
    try:
        # Obtener datos del JSON
        data = request.get_json()
        nombre = data.get('nombre')

        # Validar que el nombre no esté vacío
        if not nombre or nombre.strip() == '':
            return jsonify({'Error': 'El nombre para crear la categoría es obligatorio.'}), 400

        # Llamar a la función para crear la categoría
        id_categoria = crear_categoria(nombre)

        # Devolver el ID de la categoría creada
        return jsonify({'idCategoria': id_categoria}), 201

    except ValueError as ve:
        # Manejar errores de validación específicos
        return jsonify({'Error': str(ve)}), 400

    except Exception as e:
        # Manejar errores inesperados
        return jsonify({'Error': 'Hubo un problema al crear la categoría. Verifica su servidor y notifique al administrador.'}), 500

# -----------------------------------------------------------------------------------------------------------------------

@categories.route('/categorias/<int:id>', methods=['PUT'])
def update_categoria(id):
    try:
        data = request.get_json()
        nombre = data.get('nombre')

        # Validar que el nombre no esté vacío
        if not nombre or nombre.strip() == '':
            return jsonify({'Error': 'El nombre para editar la categoría es obligatorio.'}), 400

        resultado = actualizar_categoria(id, nombre)
        if resultado == 'sin_cambio':
            return jsonify({'message': 'La categoría ya tenía el nombre proporcionado. No se realizaron cambios.'}), 200
        elif resultado:
            return jsonify({'message': 'Categoría actualizada correctamente.'}), 200
        else:
            return jsonify({'Error': f'No se encontró la categoría con ID {id}.'}), 404
    except ValueError as ve:
        return jsonify({'Error': str(ve)}), 400
    except Exception as e:
        # Para más detalles en caso de error
        return jsonify({'Error': 'Hubo un problema al actualizar la categoría. Verifica su servidor y notifique al administrador.'}), 500
    
    # -----------------------------------------------------------------------------------------------------------------------

@categories.route('/categorias/<int:id>', methods=['DELETE'])
def delete_categoria(id):
    try:
        resultado = eliminar_categoria(id)
        if resultado == 'productos_asociados':
            return jsonify({'Error': 'No se puede eliminar la categoría porque tiene productos asociados.'}), 400
        elif resultado == 'no_encontrado':
            return jsonify({'Error': 'Categoría no encontrada.'}), 404
        else:
            return jsonify({'message': 'Categoría eliminada correctamente.'}), 200
    except Exception as e:
        return jsonify({'Error': 'Hubo un problema al eliminar la categoría. Verifique su servidor.'}), 500
    
# -----------------------------------------------------------------------------------------------------------------------

# OBTENER INFORMACION DE CATEGORIAS MEDIANTE SU NOMBRE CON SIMILITUD ---------------------------------------
@categories.route('/info_categorias_similitud/<nombre_categoria>', methods=['GET'])
def get_info_categorias_similitud(nombre_categoria):
    try:
        # Obtén las categorías similares
        categorias_similares = obtener_categorias_similares(nombre_categoria)

        # Devuelve una lista vacía si no se encuentran categorías similares
        if categorias_similares is None or len(categorias_similares) == 0:
            return jsonify([])

        # Devuelve la lista de categorías similares
        return jsonify(categorias_similares)
    except Exception as e:
        return jsonify({'error': str(e)}), 500