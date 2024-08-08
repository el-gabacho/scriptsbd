from flask import Blueprint, request, jsonify
from models import MarcaSchema
from sqlalchemy.exc import ProgrammingError
from service.inventario import buscar_inventarios, get_productos, get_producto, obtener_stock_bajo, crear_producto, eliminar_producto
from service.vehiculos import get_marcas_con_count_modelos, obtener_marca, obtener_modelo_anio_con_count, relaciona_modelo_anio
from service.categorias import obtener_categorias, crear_categoria, eliminar_categoria, actualizar_categoria
from service.proveedores import obtener_proveedores, obtener_proveedor, crear_proveedor, eliminar_proveedor, actualizar_proveedor
from service.usuarios import obtener_usuarios, obtener_usuario, crear_usuario, eliminar_usuario, actualizar_usuario
from service.ventas import obtener_ventas, obtener_detalle_venta, obtener_ventas_totales_por_usuario_fechas, crear_venta, revertir_venta, revertir_venta_producto, modificar_venta_producto

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
    
@routes.route('/stock_bajo', methods=['GET'])
def get_stock_bajo():
    try:
        stock_bajo = obtener_stock_bajo()
        return jsonify(stock_bajo)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@routes.route('/productos', methods=['POST'])
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

@routes.route('/productos/<int:id>', methods=['DELETE'])
def delete_producto(id):
    try:
        # Llamar a la función para eliminar el producto
        eliminar_producto(id)
        return jsonify({'message': 'Producto eliminado correctamente'})
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

@routes.route('/categorias', methods=['GET'])
def get_categorias():
    try:
        categorias = obtener_categorias()
        return jsonify(categorias)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@routes.route('/categorias', methods=['POST'])
def create_categoria():
    try:
        data = request.get_json()
        nombre = data.get('nombre')
        id_categoria = crear_categoria(nombre)
        return jsonify({'idCategoria': id_categoria}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@routes.route('/categorias/<int:id>', methods=['DELETE'])
def delete_categoria(id):
    try:
        eliminar_categoria(id)
        return jsonify({'message': 'Categoría eliminada correctamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@routes.route('/categorias/<int:id>', methods=['PUT'])
def update_categoria(id):
    try:
        data = request.get_json()
        nombre = data.get('nombre')
        actualizar_categoria(id, nombre)
        return jsonify({'message': 'Categoría actualizada correctamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@routes.route('/proveedores', methods=['GET'])
def get_proveedores():
    try:
        proveedores = obtener_proveedores()
        return jsonify(proveedores)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@routes.route('/proveedores/<int:id>', methods=['GET'])
def get_proveedor(id):
    try:
        proveedor = obtener_proveedor(id)
        if proveedor:
            return jsonify(proveedor)
        return jsonify({'message': 'Proveedor no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@routes.route('/proveedores', methods=['POST'])
def crearte_proveedor():
    try:
        data = request.get_json()
        nombre = data.get('nombre')
        encargado = data.get('encargado')
        telefono = data.get('telefono')
        correo = data.get('correo')
        id_proveedor = crear_proveedor(nombre, encargado, telefono, correo)
        return jsonify({'idCategoria': id_proveedor}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@routes.route('/proveedores/<int:id>', methods=['DELETE'])
def delete_proveedor(id):
    try:
        eliminar_proveedor(id)
        return jsonify({'message': 'Proveedor eliminado correctamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@routes.route('/proveedores/<int:id>', methods=['PUT'])
def update_proveedor(id):
    try:
        data = request.get_json()
        nombre = data.get('nombre')
        encargado = data.get('encargado')
        telefono = data.get('telefono')
        correo = data.get('correo')
        response = actualizar_proveedor(id, nombre, encargado, telefono, correo)
        return jsonify({'message': 'Proveedor actualizado correctamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@routes.route('/usuarios', methods=['GET'])
def get_usuarios():
    try:
        usuarios = obtener_usuarios()
        return jsonify(usuarios)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@routes.route('/usuarios/<int:id>', methods=['GET'])
def get_usuario(id):
    try:
        usuario = obtener_usuario(id)
        if usuario:
            return jsonify(usuario)
        return jsonify({'message': 'Usuario no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@routes.route('/usuarios', methods=['POST'])
def create_usuario():
    try:
        data = request.get_json()
        nombre = data.get('nombre')
        usuario = data.get('usuario')
        contrasena = data.get('contrasena')
        idRol = data.get('idRol')
        id_usuario = crear_usuario(nombre, usuario, contrasena, idRol)
        return jsonify({'idUsuario': id_usuario}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@routes.route('/usuarios/<int:id>', methods=['DELETE'])
def delete_usuario(id):
    try:
        eliminar_usuario(id)
        return jsonify({'message': 'Usuario eliminado correctamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@routes.route('/usuarios/<int:id>', methods=['PUT'])
def update_usuario(id):
    try:
        data = request.get_json()
        nombre = data.get('nombre')
        usuario = data.get('usuario')
        contrasena = data.get('contrasena')
        idRol = data.get('idRol')
        actualizar_usuario(id, nombre, usuario, contrasena, idRol)
        return jsonify({'message': 'Usuario actualizado correctamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@routes.route('/ventas', methods=['GET'])
def get_ventas():
    try:
        id_usuario = request.args.get('IdUsuario', None)
        fecha = request.args.get('Fecha', None)
        
        filtros = {
            'idUsuario': id_usuario,
            'fecha': fecha
        }
        ventas = obtener_ventas(filtros)
        return jsonify(ventas)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@routes.route('/ventas/<int:id>/productos', methods=['GET'])
def get_detalle_venta(id):
    try:
        detalle_venta = obtener_detalle_venta(id)
        if detalle_venta:
            return jsonify(detalle_venta)
        return jsonify({'message': 'Detalle de venta no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@routes.route('/ventas/usuario', methods=['GET'])
def get_ventas_totales_por_usuario_fechas():
    try:
        id_usuario = request.args.get('id_usuario', None)
        fecha_inicio = request.args.get('fecha_inicio', None)
        fecha_fin = request.args.get('fecha_fin', None)
        
        filtros = {
            'usuario': id_usuario,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin
        }
        ventas_totales = obtener_ventas_totales_por_usuario_fechas(filtros)
        return jsonify(ventas_totales)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@routes.route('/ventas', methods=['POST'])
def create_venta():
    try:
        data = request.get_json()
        idUsuario = data.get('id_usuario')
        idCliente = data.get('id_cliente')
        productos = data.get('productos')
        montoTotal = data.get('monto_total')
        recibioDinero = data.get('recicio_dinero')
        folioTicket = data.get('folio_ticket')
        imprimioTicket = data.get('imprimio_ticket')
        idTipoPago = data.get('id_tipo_pago')
        referenciaUnica = data.get('referencia_unica')
        id_venta = crear_venta(idUsuario, idCliente, productos, montoTotal, recibioDinero, folioTicket, imprimioTicket, idTipoPago, referenciaUnica)
        return jsonify({'idVenta': id_venta}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@routes.route('/ventas/<int:id>', methods=['DELETE'])
def reverse_venta(id):
    try:
        revertir_venta(id)
        return jsonify({'message': 'Venta eliminada correctamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@routes.route('/ventas/<int:ventaId>/productos/<int:productoId>', methods=['DELETE'])
def reverse_venta_producto(ventaId,productoId):
    try:
        revertir_venta_producto(ventaId,productoId)
        return jsonify({'message': 'Producto eliminado de la venta correctamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@routes.route('/ventas/<int:ventaId>/productos/<int:productoId>', methods=['PUT'])
def update_venta_producto(ventaId,productoId):
    try:
        data = request.get_json()
        cantidad = data.get('cantidad')
        tipoVenta = data.get('tipoVenta')
        precioVenta = data.get('precio')
        response = modificar_venta_producto(ventaId,productoId,tipoVenta,cantidad,precioVenta)
        return jsonify({'message': 'Producto actualizado de la venta correctamente'})
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500