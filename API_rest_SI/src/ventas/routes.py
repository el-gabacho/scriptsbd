from flask import request, jsonify
from ventas.funciones import obtener_ventas, obtener_detalle_venta, obtener_ventas_totales_por_usuario_fechas, crear_venta,\
      revertir_venta, revertir_venta_producto, modificar_venta_producto, obtener_venta_preciso
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
        return jsonify({'error': 'Ocurrió un problema al obtener las ventas. Por favor, inténtalo más tarde.'}), 500
    
@routes.route('/venta_preciso/<ticket>', methods=['GET'])
def get_venta_preciso(ticket):
    try:
        venta_preciso = obtener_venta_preciso(ticket)
        # Devuelve un mensaje si no se encuentra el producto
        if venta_preciso is None or len (venta_preciso) == 0:
            return jsonify(None)
        
        return jsonify(venta_preciso)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@routes.route('/ventas/<int:id>/productos', methods=['GET'])
def get_detalle_venta(id):
    try:
        detalle_venta = obtener_detalle_venta(id)
        if detalle_venta:
            return jsonify(detalle_venta)
        return jsonify({'error': 'Detalle de venta no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': 'Ocurrió un problema al obtener los productos de la venta {id}. Por favor, inténtalo más tarde.'}), 500

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
        return jsonify({'error': 'Ocurrió un problema al obtener las ventas del usuario {id_usuario}. Por favor, inténtalo más tarde.'}), 500

@routes.route('/ventas', methods=['POST'])
def create_venta():
    try:
        data = request.get_json()
        idUsuario = data.get('idUsuario')
        idCliente = data.get('idCliente')
        productos = data.get('productos')
        montoTotal = data.get('montoTotal')
        recibioDinero = data.get('reciboDinero')
        folioTicket = data.get('folio')
        imprimioTicket = data.get('imprimioTicket')
        idTipoPago = data.get('idTipoPago')
        referenciaUnica = data.get('referencia')
        
        if not idUsuario or not idCliente or not productos or not montoTotal or not recibioDinero or not folioTicket or not imprimioTicket or not idTipoPago:
            return jsonify({'error': 'Faltan datos para crear la venta'}), 400
        if not referenciaUnica:
            referenciaUnica = 'NO APLICA'
        id_venta = crear_venta(idUsuario, idCliente, productos, montoTotal, recibioDinero, folioTicket, imprimioTicket, idTipoPago, referenciaUnica)
        return jsonify({'idVenta': id_venta}), 201
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'error': 'Hubo un problema al crear la venta. Verifica su servidor y notifique al administrador.'}), 500
    
@routes.route('/ventas/<int:id>', methods=['DELETE'])
def reverse_venta(id):
    try:
        revertir_venta(id)
        return jsonify({'message': 'Venta eliminada correctamente'})
    except Exception as e:
        return jsonify({'error': 'Hubo un problema al revertir la venta. Verifica su servidor y notifique al administrador.'}), 500

@routes.route('/ventas/<int:ventaId>/productos/<int:productoId>', methods=['DELETE'])
def reverse_venta_producto(ventaId,productoId):
    try:
        revertir_venta_producto(ventaId,productoId)
        return jsonify({'message': 'Producto eliminado de la venta correctamente'})
    except Exception as e:
        return jsonify({'error': 'Hubo un problema al  el producto de la venta {ventaId}. Verifica su servidor y notifique al administrador.'}), 500
    
@routes.route('/ventas/<int:ventaId>/productos/<int:productoId>', methods=['PUT'])
def update_venta_producto(ventaId,productoId):
    try:
        data = request.get_json()
        cantidad = data.get('cantidad')
        tipoVenta = data.get('tipoVenta')
        precioVenta = data.get('precio')
        
        if not cantidad or not tipoVenta or not precioVenta:
            return jsonify({'error': 'Faltan datos para modificar el producto de la venta'}), 400
        
        response = modificar_venta_producto(ventaId,productoId,tipoVenta,cantidad,precioVenta)
        return jsonify({'message': 'Producto actualizado de la venta correctamente'})
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'error': 'Hubo un problema al actualizar la venta. Verifica su servidor y notifique al administrador.'}), 500