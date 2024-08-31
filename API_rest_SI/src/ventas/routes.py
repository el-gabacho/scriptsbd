from flask import request, jsonify
from ventas.funciones import obtener_ventas, obtener_detalle_venta, obtener_ventas_totales_por_usuario_fechas, crear_venta, revertir_venta, revertir_venta_producto, modificar_venta_producto
from ventas import sales as routes

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
            'id_usuario': id_usuario,
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
        return jsonify({'error': str(e)}), 500