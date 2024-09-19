from flask import jsonify, request
from sqlalchemy.exc import ProgrammingError
from vehiculos.funciones import get_marcas_count_modelos, get_buscar_marcas_similar, \
    crear_marca, editar_marca, eliminar_marca, get_modelos_count_productos, get_buscar_modelos_similar, \
    crear_modelo, editar_modelo, eliminar_modelo, obtener_datos_modelo_autopartes
from vehiculos import vehicles

# -----------------------------------------------------------------------------------------------------------------------------------

# CONSULTA PRINCIPAL DE VEHICULOS : MARCAS

@vehicles.route('/marcas_numero_modelos', methods=['GET'])
def get_marcas_with_model_count():
    try:
        marcas = get_marcas_count_modelos()
        return jsonify(marcas), 200
    except Exception as e:
        return jsonify({'error': 'Ocurrió un problema al obtener las marcas. Por favor, verifique su servidor.'}), 500


# -----------------------------------------------------------------------------------------------------------------------------------
# CRUD DE MARCA: BUSCAR POR NOMBRE DE LA MARCA, CREAR NUEVA MARCA, EDITAR MARCA Y ELIMINAR MARCA

# BUSCAR POR NOMBRE DE LA MARCA SIMILITUD
@vehicles.route('/buscar_marca_similar/<string:nombremarca>', methods=['GET'])
def search_marca_similar(nombremarca):
    try:
        marcas = get_buscar_marcas_similar(nombremarca)
        
        # Devuelve una lista vacía si no se encuentran productos similares
        if marcas is None or len(marcas) == 0:
            return jsonify([])
        
        # Devuelve la lista de productos similares
        return jsonify(marcas)
    
    except Exception as e:
        return jsonify({'error': 'Ocurrió un problema al obtener las categorías. Por favor, verifique su servidor.'}), 500

# -----------------------------------------------------------------------------------------------------------------------------------

# CREAR UNA NUEVA MARCA
@vehicles.route('/nueva_marca', methods=['POST'])
def create_marca():
    try:
        data = request.get_json()
        nombre = data.get('nombre')
        urlLogo = data.get('urlLogo', None)

        # Validar que el nombre no esté vacío
        if not nombre or nombre.strip() == '':
            return jsonify({'error': 'El nombre de la marca es obligatorio.'}), 400

        # Llamar a la función para crear la marca y manejar el resultado
        resultado = crear_marca(nombre, urlLogo)

        if resultado == 'marca_ya_existe':
            return jsonify({'error': f'La marca con el nombre "{nombre}" ya existe.'}), 400
        elif resultado == 'creacion_exitosa':
            return jsonify({'message': 'Marca creada exitosamente.'}), 201

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'error': 'Hubo un problema en el servidor. Verifica su servidor y notifique al administrador.'}), 500

# -----------------------------------------------------------------------------------------------------------------------

# EDITAR UNA MARCA
@vehicles.route('/editar_marca/<int:id>', methods=['PUT'])
def update_marca(id):
    try:
        data = request.get_json()
        nombre = data.get('nombre')
        urlLogo = data.get('urlLogo', None)  # Permitir None si no se proporciona

        # Validación: El nombre de la marca es obligatorio
        if not nombre or nombre.strip() == '':
            return jsonify({'error': 'El nombre de la marca es obligatorio.'}), 400

        # Intentar editar la marca
        resultado = editar_marca(id, nombre, urlLogo)

        # Si la marca no se encontró
        if not resultado:
            return jsonify({'error': f'No se encontró la marca con ID {id}.'}), 404

        # Si se devolvió un mensaje de que la marca ya existe
        if resultado == 'ya_existe':
            return jsonify({'error': f'Ya existe una marca con el nombre de "{nombre}".'}), 400

        # Si no se hicieron cambios porque el nombre es el mismo
        if resultado == 'sin_cambio':
            return jsonify({'message': 'No se realizaron cambios, el nombre es el mismo.'}), 200

        # Si todo salió bien, devolver mensaje de éxito
        return jsonify({'message': 'Marca actualizada correctamente.'}), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400

    except Exception as e:
        return jsonify({'error': 'Hubo un problema en el servidor. Verifica su servidor y notifique al administrador.'}), 500

# -----------------------------------------------------------------------------------------------------------------------

# ELIMINAR UNA MARCA
@vehicles.route('/eliminar_marca/<int:id>', methods=['DELETE'])
def delete_marca(id):
    try:
        # Llamar a la función para eliminar la marca
        resultado = eliminar_marca(id)
        
        if resultado == 'marca_no_encontrada':
            return jsonify({'error': f'No se encontró la marca con ID {id}.'}), 404
        elif resultado == 'marca_tiene_referencias':
            return jsonify({'error': 'No se puede eliminar la marca porque tiene modelos asociados.'}), 409
        else:
            return jsonify({'message': 'Marca eliminada correctamente.'}), 200
    except Exception as e:
        return jsonify({'error': 'Hubo un problema en el servidor. Verifica su servidor y notifique al administrador.'}), 500

# -----------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------

# CONSULTA SECUNDARIA DE VEHICULOS : MARCAS (ID) : MODELOS

@vehicles.route('/modelos_numero_productos/<int:id>', methods=['GET'])
def get_modelos_with_productos_count(id):
    try:
        modelo = get_modelos_count_productos(id)
        return jsonify(modelo)
    except Exception as e:
        return jsonify({'error': 'Ocurrió un problema al obtener los modelos de la marca. Por favor, verifique su servidor.'}), 500

# -----------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------
# CRUD DE MODELO: BUSCAR POR NOMBRE DEL MODELO, CREAR NUEVO MODELO, EDITAR MODELO Y ELIMINAR MODELO

@vehicles.route('/buscar_modelo_similar/<int:id>/<string:nombremodelo>', methods=['GET'])
def search_modelo_similar(id, nombremodelo):
    try:
        modelo = get_buscar_modelos_similar(id, nombremodelo)
        
        # Devuelve una lista vacía si no se encuentran productos similares
        if modelo is None or len(modelo) == 0:
            return jsonify([])
        
        # Devuelve la lista de productos similares
        return jsonify(modelo)
    
    except Exception as e:
        return jsonify({'error': 'Ocurrió un problema al obtener los modelos de la marca. Por favor, verifique su servidor.'}), 500

# -----------------------------------------------------------------------------------------------------------------------
    
# CREAR UN NUEVO MODELO
@vehicles.route('/crear_modelo', methods=['POST'])
def create_modelo():
    try:
        data = request.get_json()
        idMarca = data.get('idMarca')
        print(f"se obtiene : {idMarca}")
        nombre = data.get('nombre')
        print(f"se obtiene : {nombre}")

        # Validar que el nombre del modelo no esté vacío
        if not nombre or nombre.strip() == '':
            return jsonify({'error': 'El nombre del modelo es obligatorio.'}), 400

        # Llamar a la función de creación de modelo
        resultado = crear_modelo(idMarca, nombre)
        
        # Verificar el resultado y devolver los mensajes correspondientes
        if resultado == 'marca_no_encontrada':
            return jsonify({'error': f'No se encontró la marca con ID {idMarca}.'}), 404
        elif resultado == 'modelo_existente':
            return jsonify({'error': f'Ya existe un modelo con el nombre "{nombre}" para la marca proporcionada.'}), 409
        else:
            return jsonify({'message': 'Modelo creado correctamente', 'idModelo': resultado}), 201

    except Exception as e:
        return jsonify({'error': 'Ocurrió un problema al crear el modelo. Por favor, verifique su servidor.'}), 500

# -----------------------------------------------------------------------------------------------------------------------

# EDITAR UN MODELO
@vehicles.route('/editar_modelo/<int:id>', methods=['PUT'])
def update_modelo(id):
    try:
        data = request.get_json()
        nombre = data.get('nombre')
        
        # Validar que el nombre no esté vacío
        if not nombre or nombre.strip() == '':
            return jsonify({'error': 'El nombre del modelo es obligatorio.'}), 400

        # Intentar editar el modelo
        resultado = editar_modelo(id, nombre)
        
        if resultado == 'sin_cambio':
            return jsonify({'error': 'El modelo ya tenía el nombre proporcionado. No se realizaron cambios.'}), 200
        elif resultado:
            return jsonify({'message': 'Modelo actualizado correctamente'}), 200
        else:
            return jsonify({'error': f'No se encontró el modelo con ID {id}.'}), 404

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'error': 'Ocurrió un problema al actualizar el modelo. Por favor, verifique su servidor.'}), 500

# -----------------------------------------------------------------------------------------------------------------------

# ELIMINAR UNA MARCA
@vehicles.route('/eliminar_modelo/<int:id>', methods=['DELETE'])
def delete_modelo(id):
    try:
        # Intentar eliminar el modelo y obtener el resultado
        resultado = eliminar_modelo(id)
        
        if resultado == 'no_encontrado':
            return jsonify({'error': f'No se encontró el modelo con ID {id}.'}), 404
        elif resultado == 'tiene_productos':
            return jsonify({'error': 'El modelo tiene productos asociados y no se puede eliminar.'}), 409
        else:
            return jsonify({'message': 'Modelo eliminado correctamente'}), 200

    except Exception as e:
        return jsonify({'error': 'Ocurrió un problema al eliminar el modelo. Por favor, verifique su servidor.'}), 500
    
@vehicles.route('/vehiculos/<int:idInventario>', methods=['GET'])
def get_vehiculos(idInventario):
    try:
        vehiculos = obtener_datos_modelo_autopartes(idInventario)
        return jsonify(vehiculos), 200
    except Exception as e:
        print(e)
        return jsonify({'error': 'Ocurrió un problema al obtener los vehículos.'}), 500