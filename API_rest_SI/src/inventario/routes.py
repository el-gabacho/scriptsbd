from flask import jsonify, request, send_file
from inventario.funciones import get_productos, get_producto_preciso, get_productos_similares, get_productos_avanzada,\
    obtener_stock_bajo, get_productos_eliminados, crear_producto, modificar_producto, eliminar_producto, reactivar_producto,\
    agregar_existencias_producto, obtener_imagen
from inventario.func_importar import importar_productos
from inventario import inventory as routes
from PIL import Image
import io
import os
from werkzeug.utils import secure_filename

# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------

# TODOS LOS PRODUCTOS CON INFORMACION
@routes.route('/info_productos', methods=['GET'])
def get_info_productos():
    try:
        productos = get_productos()
        return jsonify(productos)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# UN PRODUCTO CON TODA INFORMACION CON CODIGO FIJO
@routes.route('/info_productos_preciso/<codigo_barras>', methods=['GET'])
def get_info_productos_preciso_by(codigo_barras):
    try:
        producto_preciso = get_producto_preciso(codigo_barras)
        return jsonify(producto_preciso)
    except Exception as e:
        print(f"Error en get_info_productos_preciso_by: {str(e)}")
        return jsonify({'error': str(e)}), 500
    
# TODOS LOS PRODUCTOS CON INFORMACION CON CODIGO SIMILAR
@routes.route('/info_productos_similitud/<codigo_barras>', methods=['GET'])
def get_info_productos_similar_by(codigo_barras):
    try:
        # Obtén los productos similares
        producto_similar = get_productos_similares(codigo_barras)

        # Devuelve una lista vacía si no se encuentran productos similares
        if producto_similar is None or len(producto_similar) == 0:
            return jsonify([])

        # Devuelve la lista de productos similares
        return jsonify(producto_similar)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# TODOS LOS PRODUCTOS CON INFORMACION DE CIERTO CAMPOS SIMILARES
@routes.route('/productos_busqueda_avanzada/', methods=['GET'])
def get_productos_busqueda_avanzada():
    try:
        # Obtener los parámetros de consulta de la solicitud GET
        codigoBarras = request.args.get('codigoBarras', None)
        nombre = request.args.get('nombre', None)
        descripcion = request.args.get('descripcion', None)
        categoria = request.args.get('categoria', None)
        proveedor = request.args.get('proveedor', None)
        marca = request.args.get('marca', None)
        modelo = request.args.get('modelo', None)
        fecha_inicio = request.args.get('fecha_inicio', None)
        fecha_fin = request.args.get('fecha_fin', None)
        anio_todo = request.args.get('anio_todo', None)

        # Convertir anio_todo a tipo booleano si es necesario
        if anio_todo is not None:
            try:
                anio_todo = bool(int(anio_todo))  # Asumiendo que anio_todo es 0 o 1
            except ValueError:
                anio_todo = None  # Manejar el caso en que anio_todo no se puede convertir

        # Crear un diccionario de filtros
        filtros = {
            'codigo': codigoBarras,
            'nombre': nombre,
            'descripcion': descripcion,
            'categoria': categoria,
            'proveedor': proveedor,
            'marca': marca,
            'modelo': modelo,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'anio_todo': anio_todo
        }

        # Llamar a la función de búsqueda con los filtros
        inventario_avanzado = get_productos_avanzada(filtros)

        # Devuelve una lista vacía si no se encuentran productos similares
        if inventario_avanzado is None or len(inventario_avanzado) == 0:
            return jsonify([])

        return jsonify(inventario_avanzado)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

# TODOS LOS PRODUCTOS CON INFORMACION CON STOCK BAJO    
@routes.route('/productos_bajo', methods=['GET'])
def get_stock_bajo():
    try:
        stock_bajo = obtener_stock_bajo()

        # Devuelve una lista vacía si no se encuentran productos similares
        if stock_bajo is None or len(stock_bajo) == 0:
            return jsonify([])
        
        return jsonify(stock_bajo)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# TODOS LOS PRODUCTOS CON INFORMACION CON STOCK BAJO    
@routes.route('/productos_eliminados', methods=['GET'])
def get_producto_eliminado():
    try:
        codigoBarras = request.args.get('codigo_barras', None)
        print(f"Received data: {codigoBarras}")  # Verifica los datos recibidos
        eliminado_producto = get_productos_eliminados(codigoBarras)

        # Devuelve una lista vacía si no se encuentran productos similares
        if eliminado_producto is None or len(eliminado_producto) == 0:
            return jsonify([])
        
        return jsonify(eliminado_producto)
    except Exception as e:
        print(f"Error en get_producto_eliminado: {str(e)}")
        return jsonify({'error': str(e)}), 500
    
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------

# CREAR UN PRODUCTO
@routes.route('/nuevo_producto', methods=['POST'])
def create_producto():
    try:
        # Obtener los datos del producto del cuerpo de la solicitud POST
        data = request.get_json()
        print("Datos recibidos:", data)  # Agregar para depuración
        
        # Extraer los datos del JSON
        codigoBarras = data.get('codigo')
        nombre = data.get('nombre')
        descripcion = data.get('descripcion')
        cantidadActual = data.get('existencias')
        cantidadMinima = data.get('cantidadMinima')
        precioCompra = data.get('precioCompra')
        mayoreo = data.get('precioMayoreo')
        menudeo = data.get('precioMenudeo')
        colocado = data.get('precioColocado')
        idUnidadMedida = data.get('idUnidadMedida')
        idProveedor = data.get('idProveedor')
        idCategoria = data.get('idCategoria')
        idUsuario = data.get('idUsuario')
        imagenes = data.get('imagenes')
        
        # Extraer la lista de vehículos
        vehiculos = data.get('vehiculos', [])  # Definir valor por defecto vacío en caso de que no se proporcione
        print("Vehículos recibidos:", vehiculos)  # Agregar para depuración

        # Llamar a la función para crear el producto
        id_inventario = crear_producto(
            codigoBarras, nombre, descripcion, cantidadActual, cantidadMinima,
            precioCompra, mayoreo, menudeo, colocado, idUnidadMedida, idCategoria,
            idProveedor, idUsuario, imagenes, vehiculos)

        if isinstance(id_inventario, dict) and 'error' in id_inventario:
            return jsonify({'error': id_inventario['error']}), 500

        return jsonify({'idInventario': id_inventario}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@routes.route('/nuevo_producto/imagenes', methods=['POST'])
def upload_files():
    try:
        if 'files' not in request.files:
            return jsonify({'message': 'No file part in the request'}), 400

        files = request.files.getlist('files')

        for file in files:
            if file.filename == '':
                return jsonify({'message': 'No file selected for uploading'}), 400

            if file:
                filename = secure_filename(file.filename)
                file.save(os.path.join('C:\\imagenes_el_gabacho\\productosInventario', filename))
    except Exception as e:
        print(e)
        return jsonify({'message': 'Allowed file types are .webp'}), 400
    return jsonify({'message': 'Files successfully uploaded'}), 200

# MODIFICAR UN PRODUCTO
@routes.route('/modificar_producto', methods=['PUT'])
def modificar_producto_route():
    try:
        # Obtener los datos enviados en el cuerpo de la solicitud
        data = request.get_json()
        print("Datos recibidos:", data)  # Agregar para depuración

        # Extraer los valores necesarios del JSON recibido
        idInventario = data.get('idInventario')
        codigoBarras = data.get('codigoBarras')
        nombre = data.get('nombre')
        descripcion = data.get('descripcion')
        cantidadActual = data.get('cantidadActual')
        cantidadMinima = data.get('cantidadMinima')
        precioCompra = data.get('precioCompra')
        mayoreo = data.get('mayoreo')
        menudeo = data.get('menudeo')
        colocado = data.get('colocado')
        idUnidadMedida = data.get('idUnidadMedida')
        idCategoria = data.get('idCategoria')
        idProveedor = data.get('idProveedor')
        imagenes = data.get('imagenes')
        vehiculos = data.get('vehiculos')

        # Validar que el ID del producto esté presente
        if not idInventario:
            return jsonify({'error': 'ID del producto no proporcionado'}), 400

        # Llamar a la función que realiza la modificación del producto
        resultado = modificar_producto(idInventario, codigoBarras, nombre, descripcion, cantidadActual, cantidadMinima,
                                       precioCompra, mayoreo, menudeo, colocado, idUnidadMedida, idCategoria,
                                       idProveedor, imagenes, vehiculos)

        # Retornar una respuesta con el ID del producto modificado
        return jsonify({'message': 'Producto modificado correctamente', 'idInventario': resultado}), 200

    except Exception as e:
        # En caso de un error, devolver una respuesta con el error
        return jsonify({'error': str(e)}), 500


# ELIMINAR UN PRODUCTO

@routes.route('/eliminar_producto', methods=['DELETE'])
def eliminar_producto_route():
    try:
        # Obtener datos del cuerpo de la solicitud JSON
        data = request.get_json()
        print(f"Received data: {data}")  # Verifica los datos recibidos
        # Extraer 'idInventario' y 'idUsuario' del cuerpo de la solicitud
        idInventario = data.get('IdInventario')
        print(f"primer parametro ={idInventario}")
        idUsuario = data.get('IdUsuario')
        print(f"segundo parametro ={idUsuario}")
        # Llamar a la función para eliminar el producto
        resultado = eliminar_producto(idInventario, idUsuario)
        return jsonify(resultado), 200
    except Exception as e:
        print(f"Error en eliminar_producto_route: {str(e)}")
        return jsonify({'error': str(e)}), 500
    

# REACTIVAR UN PRODUCTO MEDIANTE SU ID
@routes.route('/reactivar_producto', methods=['PUT'])
def reactive_producto():
    try:
        data = request.get_json()
        print(f"Received data: {data}")  # Verifica los datos recibidos
        idInventario = data.get('IdInventario')
        print(f"primer parametro ={idInventario}")
        # Llamar a la función para reactivar el producto
        resultado = reactivar_producto(idInventario)
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# AGREGAR MAS EXISTENCIAS A UN PRODUCTO ACTIVO
@routes.route('/agregar_existencias_producto', methods=['POST'])
def agregar_existencias_producto_route():
    try:    
        # Obtener datos del cuerpo de la solicitud JSON
        data = request.get_json()
        idUsuario = data.get('idUsuario')
        idInventario = data.get('idInventario')
        cantidadNueva = data.get('cantidadNueva')
        precioCompra = data.get('precioCompra')
        mayoreo = data.get('mayoreo')
        menudeo = data.get('menudeo')
        colocado = data.get('colocado')

        # Verificación de los parámetros necesarios
        if not all([idUsuario, idInventario, cantidadNueva, precioCompra, mayoreo, menudeo, colocado]):
            return jsonify({'error': 'Todos los campos son requeridos'}), 400

        # Llamar a la función para agregar existencias
        result = agregar_existencias_producto(idUsuario, idInventario, cantidadNueva, precioCompra, mayoreo, menudeo, colocado)

        # Verificar si hubo un error durante la operación
        if 'error' in result:
            return jsonify(result), 500

        return jsonify(result), 200

    except Exception as e:
        # Manejo de cualquier excepción no esperada
        print(f"Error en agregar_existencias_producto_route: {str(e)}")
        return jsonify({'error': str(e)}), 500

# ---------------------------------------------------------------------------------------------
# IMPORTAR PRODUCTOS desde un archivo CSV
@routes.route('/importar_productos/<int:usuarioId>', methods=['POST'])
def importar_productos_csv(usuarioId):
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400
        # Obtener el archivo CSV del cuerpo de la solicitud POST
        archivo = request.files.get('file')
        
        if archivo.filename == '':
            return jsonify({'error': 'No file selected for uploading'}), 400
        
        if archivo:
            # Guardar el archivo en el directorio de archivos temporales
            ruta_archivo = os.path.join('C:\\Users\\VALENCIA\\Documents\\proyectos\\el-gabacho\\files', archivo.filename)
            archivo.save(ruta_archivo)
            
            resultado = importar_productos(ruta_archivo, usuarioId)
        
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@routes.route('/images/<int:idInventario>/<int:imagenId>')
def get_image(idInventario, imagenId):
    try:
        image_path = obtener_imagen(idInventario, imagenId)
        with Image.open(image_path) as img:
            img = img.convert("RGB")
            img_io = io.BytesIO()
            img.save(img_io, 'JPEG')
            img_io.seek(0)
        
        return send_file(img_io, mimetype='image/jpeg')
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
