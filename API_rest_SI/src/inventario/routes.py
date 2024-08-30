from flask import jsonify, request
from inventario.funciones import get_productos, get_producto_preciso, get_productos_similares, buscar_inventarios\
    , obtener_stock_bajo,crear_producto, eliminar_producto
from inventario.func_importar import importar_productos
from inventario import inventory as routes
import os

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

# TODOS LOS PRODUCTOS CON INFORMACION CON INFORMACION DE CIERTOS CAMPOS SIMILAR
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
        anio = request.args.get('anio', None)

        # Crear un diccionario de filtros
        filtros = {
            'codigoBarras': codigoBarras,
            'nombre': nombre,
            'descripcion': descripcion,
            'categoria': categoria,
            'proveedor': proveedor,
            'marca': marca,
            'modelo': modelo,
            'anio': anio
        }

        # Llamar a la función de búsqueda con los filtros
        inventarios = buscar_inventarios(filtros)
        return jsonify(inventarios)
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
        
        # Extraer los datos del JSON
        codigoBarras = data['codigo']
        nombre = data['nombre']
        descripcion = data['descripcion']
        cantidadActual = data['existencias']
        cantidadMinima = data['cantidadMinima']
        precioCompra = data['precioCompra']
        mayoreo = data['precioMayoreo']
        menudeo = data['precioMenudeo']
        colocado = data['precioColocado']
        idUnidadMedida = data['idUnidadMedida']
        idProveedor = data['idProveedor']
        idCategoria = data['idCategoria']
        idUsuario = data['idUsuario']
        imagenes = data['imagenes']
        aplicaciones = data['aplicaciones']
        
        # Llamar a la función para crear el producto
        producto = crear_producto(codigoBarras, nombre, descripcion, cantidadActual, cantidadMinima, 
                                  precioCompra, mayoreo, menudeo, colocado, idUnidadMedida, idCategoria, 
                                  idProveedor, idUsuario, imagenes, aplicaciones)

        if isinstance(producto, dict) and 'error' in producto:
            # Si hay un error en el proceso de creación del producto
            return jsonify(producto), 400

        return jsonify({'success': 'Producto creado con éxito', 'idInventario': producto}), 201

    except Exception as e:
        # Manejo de cualquier tipo de excepción inesperada
        return jsonify({'error': 'Error interno del servidor', 'message': str(e)}), 500

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