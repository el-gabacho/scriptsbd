from sqlalchemy import func, text
from ventas.modelos import Venta, PagoVenta, TipoPago, VentaProducto, Cliente
from usuarios.modelos import Usuario
from inventario.modelos import Inventario, UnidadMedida
from init import db
from datetime import datetime

def obtener_ventas(filtros):  
      
    ventas = db.session.query(Venta.idVenta, Venta.folioTicket, PagoVenta.referenciaUnica, TipoPago.tipoPago, Venta.montoTotal, Venta.fechaVenta, Usuario.usuario)\
        .join(PagoVenta, Venta.idVenta == PagoVenta.idVenta)\
        .join(TipoPago, PagoVenta.idTipoPago == TipoPago.idTipoPago)\
        .join(Usuario, Venta.idUsuario == Usuario.idUsuario)
    
    if filtros.get('idUsuario'):
        ventas = ventas.filter(Venta.idUsuario == filtros.get('idUsuario'))
    if filtros.get('fecha'):
        fecha_formateada = datetime.strptime(filtros.get('fecha'), "%Y-%m-%dT%H:%M:%S").date()
        ventas = ventas.filter(func.DATE(Venta.fechaVenta) == fecha_formateada)
    
    ventas = ventas.all()
    
    ventas_list = []
    for venta in ventas:
        ventas_list.append({
            'Id': venta.idVenta,
            'Folio': venta.folioTicket,
            'Referencia': venta.referenciaUnica,
            'TipoPago': venta.tipoPago,
            'MontoTotal': venta.montoTotal,
            'Fecha': venta.fechaVenta.isoformat() + 'Z',
            'Usuario': venta.usuario
        })
    return ventas_list

def obtener_venta_preciso(ticket):  
    query = db.session.query(Venta.idVenta, Venta.folioTicket, PagoVenta.referenciaUnica, TipoPago.tipoPago, Venta.montoTotal, Venta.fechaVenta, Usuario.usuario
        ).join(PagoVenta, Venta.idVenta == PagoVenta.idVenta
        ).join(TipoPago, PagoVenta.idTipoPago == TipoPago.idTipoPago
        ).join(Usuario, Venta.idUsuario == Usuario.idUsuario
        ).filter(Venta.folioTicket == ticket
        ).first()
    
    # Validar que no se encontró una venta
    if query is None:
        return None
    
    # Usar 'query' para acceder a los valores
    venta = {
        'Id': query.idVenta,
        'Folio': query.folioTicket,
        'Referencia': query.referenciaUnica,
        'TipoPago': query.tipoPago,
        'MontoTotal': query.montoTotal,
        'Fecha': query.fechaVenta.isoformat() + 'Z',
        'Usuario': query.usuario
    }
    
    return venta

def crear_venta(idUsuario, idCliente, productos, montoTotal, recibioDinero, folioTicket, imprimioTicket, idTipoPago, referenciaUnica):
    session = db.session 

    try:
        with session.begin():
            db.session.execute(text(f"CALL proc_crear_venta({idUsuario}, {idCliente}, @v_idVenta)"))

            result = db.session.execute(text("SELECT @v_idVenta")).first()
            id_venta = result[0]
            for producto in productos:
                if producto['precio'] == 0:
                    raise ValueError(f'El producto {producto["codigoBarras"]} no tiene precio de venta')
                sql_agregar_producto = "CALL proc_agregar_producto_venta(:idVenta, :idInventario, :cantidad, :tipoVenta, :precio, :subtotal)"
                db.session.execute(text(sql_agregar_producto), {
                    'idVenta': id_venta,
                    'idInventario': producto['idInventario'],
                    'cantidad': producto['cantidad'],
                    'tipoVenta': producto['tipoVenta'],
                    'precio': producto['precio'],
                    'subtotal': producto['subtotal']
                })
            sql_finalizar_venta = "CALL proc_finalizar_venta(:idVenta, :montoTotal, :recibioDinero, :folioTicket, :imprimioTicket, :idTipoPago, :referenciaUnica)"
            db.session.execute(text(sql_finalizar_venta), {
                'idVenta': id_venta,
                'montoTotal': montoTotal,
                'recibioDinero': recibioDinero,
                'folioTicket': folioTicket,
                'imprimioTicket': imprimioTicket,
                'idTipoPago': idTipoPago,
                'referenciaUnica': referenciaUnica
            })

        return id_venta

    except Exception as e:
        session.rollback() 
        raise ValueError(f'Ocurrió un error: {str(e)}')

def obtener_detalle_venta(idVenta):
    detalle_venta = db.session.query(VentaProducto.idVentaProducto, Inventario.codigoBarras, Inventario.nombre, Inventario.descripcion, VentaProducto.precioVenta, VentaProducto.cantidad, UnidadMedida.tipoMedida, VentaProducto.subtotal, VentaProducto.tipoVenta)\
        .join(Inventario, VentaProducto.idInventario == Inventario.idInventario)\
        .join(UnidadMedida, Inventario.idUnidadMedida == UnidadMedida.idUnidadMedida)\
        .filter(VentaProducto.idVenta == idVenta)\
        .all()
        
    productos_list = []
    for producto in detalle_venta:
        productos_list.append({
            'id': producto.idVentaProducto,
            'idVenta': idVenta,
            'codigoBarras': producto.codigoBarras,
            'nombre': producto.nombre,
            'descripcion': producto.descripcion,
            'precio': producto.precioVenta,
            'cantidad': producto.cantidad,
            'tipoMedida': producto.tipoMedida,
            'subtotal': producto.subtotal,
            'tipoVenta': producto.tipoVenta
        })
    
    return productos_list

def obtener_ventas_totales_por_usuario_fechas(filtros):
    ventas_totales = db.session.query(Usuario.usuario, func.sum(Venta.montoTotal))\
        .join(Venta, Usuario.idUsuario == Venta.idUsuario)
        
    if filtros.get('id_usuario'):
        ventas_totales = ventas_totales.filter(Usuario.idUsuario == filtros.get('id_usuario'))
    if filtros.get('fecha_inicio') and filtros.get('fecha_fin'):
        fechaInicio = datetime.strptime(filtros.get('fecha_inicio'), "%Y-%m-%dT%H:%M:%S").date()
        fechaFin = datetime.strptime(filtros.get('fecha_fin'), "%Y-%m-%dT%H:%M:%S").date()
        ventas_totales = ventas_totales.filter(func.DATE(Venta.fechaVenta).between(fechaInicio, fechaFin))
    
    ventas_totales = ventas_totales.group_by(Usuario.usuario)
    ventas_totales = ventas_totales.all()
    
    ventas_totales_list = []
    for venta in ventas_totales:
        ventas_totales_list.append({
            'Usuario': venta[0],
            'MontoTotal': float(venta[1]) if venta[1] else 0
        })
    return ventas_totales_list

def revertir_venta(id):
    db.session.execute(text(f"CALL proc_devolver_venta({id})"))
    db.session.commit()
    return True

def revertir_venta_producto(ventaId,productoId):
    db.session.execute(text(f"CALL proc_devolver_producto({ventaId},{productoId})"))
    db.session.commit()
    return True

def modificar_venta_producto(ventaId,productoId,tipoVenta,cantidad,precioVenta):
    session = db.session 

    try:
        with session.begin():
            session.execute(text(f"CALL proc_modificar_venta_producto({ventaId},{productoId},'{tipoVenta}',{cantidad},{precioVenta})"))
            return True
    except Exception as e:
            session.rollback() 
            raise ValueError(f'Ocurrió un error: {str(e)}')