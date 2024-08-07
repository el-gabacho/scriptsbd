from sqlalchemy import func
from models import db, Venta, PagoVenta, TipoPago, VentaProducto, Usuario, Inventario, UnidadMedida
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

def crear_venta(idUsuario, idCliente, productos, montoTotal, recibioDinero, folioTicket, imprimioTicket, idTipoPago, referenciaUnica):
    db.session.execute(f"CALL proc_crear_venta({idUsuario}, {idCliente}, @v_idVenta)")
    result = db.session.execute("SELECT @v_idVenta").first()
    id_venta = result[0]
    for producto in productos:
        db.session.execute(f"CALL proc_agregar_producto_venta({id_venta}, {producto.idInventario}, {producto.cantidad}, {producto.tipoVenta}, {producto.precioVenta}, {producto.subtotal})")
    db.session.execute(f"CALL proc_finalizar_venta({id_venta}, {montoTotal}, {recibioDinero}, {folioTicket}, {imprimioTicket}, {idTipoPago}, {referenciaUnica})")
    

def obtener_ventas_por_usuario_fecha(usuario, fecha):
    fecha_formateada = datetime.strptime(fecha, "%Y-%m-%d").date()
    
    ventas = db.session.query(Venta.folioTicket, PagoVenta.referenciaUnica, TipoPago.tipoPago, Venta.montoTotal, Venta.fechaVenta, Usuario.usuario)\
        .join(PagoVenta, Venta.idVenta == PagoVenta.idVenta)\
        .join(TipoPago, PagoVenta.idTipoPago == TipoPago.idTipoPago)\
        .join(Usuario, Venta.idUsuario == Usuario.idUsuario)\
        .filter(Usuario.usuario == usuario, func.DATE(Venta.fechaVenta) == fecha_formateada)\
        .all()
    
    return ventas

def obtener_detalle_venta(idVenta):
    detalle_venta = db.session.query(VentaProducto.idVentaProducto, Inventario.codigoBarras, Inventario.nombre, Inventario.descripcion, VentaProducto.precioVenta, VentaProducto.cantidad, UnidadMedida.tipoMedida, VentaProducto.subtotal, VentaProducto.tipoVenta)\
        .join(Inventario, VentaProducto.idInventario == Inventario.idInventario)\
        .join(UnidadMedida, Inventario.idUnidadMedida == UnidadMedida.idUnidadMedida)\
        .filter(VentaProducto.idVenta == idVenta)\
        .all()
        
    productos_list = []
    for producto in detalle_venta:
        productos_list.append({
            'idVentaProducto': producto.idVentaProducto,
            'codigoBarras': producto.codigoBarras,
            'nombre': producto.nombre,
            'descripcion': producto.descripcion,
            'precioVenta': producto.precioVenta,
            'cantidad': producto.cantidad,
            'tipoMedida': producto.tipoMedida,
            'subtotal': producto.subtotal,
            'tipoVenta': producto.tipoVenta
        })
    
    return productos_list

def obtener_ventas_totales_por_usuario_fechas(usuario, fechaInicio, fechaFin):
    ventas_totales = db.session.query(Usuario.usuario, func.sum(Venta.montoTotal), Venta.fechaVenta)\
        .join(Venta, Usuario.idUsuario == Venta.idUsuario)\
        .filter(Usuario.usuario == usuario, func.DATE(Venta.fechaVenta).between(fechaInicio, fechaFin))\
        .group_by(Usuario.usuario)\
        .all()
    
    return ventas_totales