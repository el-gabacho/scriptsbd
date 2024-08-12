from sqlalchemy import func, text
from models import db, Inventario, UnidadMedida
from ventas.Domain.Venta import Venta
from ventas.Domain.PagoVenta import PagoVenta
from ventas.Domain.TipoPago import TipoPago
from ventas.Domain.VentaProducto import VentaProducto
from usuarios.Domain.Usuario import Usuario
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
    db.session.commit()

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
    ventas_totales = db.session.query(Usuario.usuario, func.sum(Venta.montoTotal), func.DATE(Venta.fechaVenta))\
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
            'MontoTotal': float(venta[1]) if venta[1] else 0,
            'Fecha': venta[2].isoformat() if venta[2] else None
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
    db.session.execute(text(f"CALL proc_modificar_venta_producto({ventaId},{productoId},'{tipoVenta}',{cantidad},{precioVenta})"))
    db.session.commit()
    return True