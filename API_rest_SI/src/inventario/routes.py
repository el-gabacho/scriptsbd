from flask import jsonify, request
from inventario.funciones import get_productos, get_producto_preciso, get_productos_similares, get_productos_avanzada,\
    obtener_stock_bajo, crear_producto, eliminar_producto
from inventario.func_importar import importar_productos
from inventario import inventory as routes
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
@routes.route('/productos_busqueda_avanzada', methods=['GET'])
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

# ELIMINAR UN PRODUCTO MEDIANTE SU ID
@routes.route('/productos/<int:id>', methods=['DELETE'])
def delete_producto(id):
    try:
        # Llamar a la función para eliminar el producto
        eliminar_producto(id)
        return jsonify({'message': 'Producto eliminado correctamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# ---------------------------------------------------------------------------------------------
# IMPORTAR PRODUCTOS desde un archivo CSV
@routes.route('/importar_productos/<int:usuarioId>', methods=['POST'])
def importar_productos_csv(usuarioId):
    try:
        if 'file' not in request.files:
            return jsonify({'message': 'No file part in the request'}), 400
        # Obtener el archivo CSV del cuerpo de la solicitud POST
        archivo = request.files.get('file')
        
        if archivo.filename == '':
            return jsonify({'message': 'No file selected for uploading'}), 400
        
        if archivo:
            # Guardar el archivo en el directorio de archivos temporales
            ruta_archivo = os.path.join('C:\\Users\\VALENCIA\\Documents\\proyectos\\el-gabacho\\files', archivo.filename)
            archivo.save(ruta_archivo)
            
            resultado = importar_productos(ruta_archivo, usuarioId)
        
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'error': str(e)}), 500