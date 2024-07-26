from flask import Blueprint, request, jsonify
from models import MarcaSchema
from sqlalchemy.exc import ProgrammingError
from service.inventario import buscar_inventarios, get_productos, get_producto, get_stock_bajo, crear_producto, eliminar_producto
from service.vehiculos import get_marcas_con_count_modelos, get_marca, get_modelo_anio_count, relaciona_modelo_anio
from service.categorias import get_categorias, crear_categoria, eliminar_categoria, actualizar_categoria
from service.proveedores import get_proveedores, get_proveedor, crear_proveedor, eliminar_proveedor, actualizar_proveedor
from service.usuarios import get_usuarios, get_usuario, crear_usuario, eliminar_usuario, actualizar_usuario
from service.ventas import obtener_ventas_por_usuario_fecha, obtener_detalle_venta, obtener_ventas_totales_por_usuario_fechas, crear_venta

routes = Blueprint('routes', __name__)

marca_schema = MarcaSchema()
marcas_schema = MarcaSchema(many=True)

@routes.route('/info_productos', methods=['GET'])
def get_info_productos():
    try:
        productos = get_productos()
        return jsonify(productos)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@routes.route('/info_productos/<codigo_barras>', methods=['GET'])
def get_info_productos_by(codigo_barras):
    try:
        producto = get_producto(codigo_barras)
        return jsonify(producto)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@routes.route('/productos_busqueda_avanzada', methods=['GET'])
def get_productos_busqueda_avanzada(filtros):
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
    
@routes.route('/marcas', methods=['GET'])
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
        marca = get_marca(id)
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
        modelos = get_modelo_anio_count(idmarca)
        return jsonify(modelos)
    except ProgrammingError as e:
        return jsonify({'error': 'Error en la estructura de la base de datos', 'details': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Ocurrió un error inesperado', 'details': str(e)}), 500

@routes.route('/categorias', methods=['GET'])
def get_categorias():
    try:
        categorias = get_categorias()
        return jsonify(categorias)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@routes.route('/proveedores', methods=['GET'])
def get_proveedores():
    try:
        proveedores = get_proveedores()
        return jsonify(proveedores)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@routes.route('/proveedores/<int:id>', methods=['GET'])
def get_proveedor(id):
    try:
        proveedor = get_proveedor(id)
        if proveedor:
            return jsonify(proveedor)
        return jsonify({'message': 'Proveedor no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@routes.route('/usuarios', methods=['GET'])
def get_usuarios():
    try:
        usuarios = get_usuarios()
        return jsonify(usuarios)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
