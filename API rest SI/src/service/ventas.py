from models import db

def crear_venta(idUsuario, idCliente, productos, montoTotal, recibioDinero, folioTicket, imprimioTicket, idTipoPago, referenciaUnica):
    db.session.execute(f"CALL proc_crear_venta({idUsuario}, {idCliente}, @v_idVenta)")
    result = db.session.execute("SELECT @v_idVenta").first()
    id_venta = result[0]
    for producto in productos:
        db.session.execute(f"CALL proc_agregar_producto_venta({id_venta}, {producto.idInventario}, {producto.cantidad}, {producto.tipoVenta}, {producto.precioVenta}, {producto.subtotal})")
    db.session.execute(f"CALL proc_finalizar_venta({id_venta}, {montoTotal}, {recibioDinero}, {folioTicket}, {imprimioTicket}, {idTipoPago}, {referenciaUnica})")