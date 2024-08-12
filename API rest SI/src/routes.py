from flask import Blueprint, request, jsonify
from models import MarcaSchema
from sqlalchemy.exc import ProgrammingError
from service.inventario import get_productos, get_producto_preciso, get_productos_similares, buscar_inventarios, obtener_stock_bajo, crear_producto, eliminar_producto
from service.vehiculos import get_marcas_con_count_modelos, obtener_marca, obtener_modelo_anio_con_count, relaciona_modelo_anio

routes = Blueprint('routes', __name__)

marca_schema = MarcaSchema()
marcas_schema = MarcaSchema(many=True)

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

# CREAR UN PRODUCTO
@routes.route('/producto', methods=['POST'])
def create_producto():
    try:
        # Obtener los datos del producto del cuerpo de la solicitud POST
        data = request.get_json()
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
        idUsuario = data.get('idUsuario')
        id_modeloAnio = data.get('id_modeloAnio')

        # Llamar a la función para crear el producto
        producto = crear_producto(codigoBarras, nombre, descripcion, cantidadActual, cantidadMinima, precioCompra, mayoreo, menudeo, colocado, idUnidadMedida, idCategoria, idProveedor, idUsuario, id_modeloAnio)
        return jsonify(producto), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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

@routes.route('/marcas_con_modelo', methods=['GET'])
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