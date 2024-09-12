from flask import request, jsonify
from categorias.funciones import obtener_categorias, crear_categoria, eliminar_categoria, actualizar_categoria
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
            return jsonify({'Error': 'La categoría ya tenía el nombre proporcionado. No se realizaron cambios.'}), 200
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
        eliminar_categoria(id)
        return jsonify({'message': 'Categoría eliminada correctamente'})
    except Exception as e:
        return jsonify({'Error': str(e)}), 500