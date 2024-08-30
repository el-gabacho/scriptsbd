from init import db

class Venta(db.Model):
    __tablename__ = 'ventas'

    idVenta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idUsuario = db.Column(db.Integer, db.ForeignKey('usuarios.idUsuario'), nullable=False)
    idCliente = db.Column(db.Integer, db.ForeignKey('clientes.idCliente'), nullable=False)
    montoTotal = db.Column(db.Float, nullable=False)
    recibioDinero = db.Column(db.Float, nullable=False)
    folioTicket = db.Column(db.String(50), nullable=False)
    imprimioTicket = db.Column(db.Boolean, nullable=False)
    fechaVenta = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())

    usuario = db.relationship('Usuario', backref='ventas')
    cliente = db.relationship('Cliente', backref='ventas')
    
class Cliente(db.Model):
    __tablename__ = 'clientes'

    idCliente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(30), nullable=False)
    
class PagoVenta(db.Model):
    __tablename__ = 'pagoVenta'

    idPagoVenta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idVenta = db.Column(db.Integer, db.ForeignKey('ventas.idVenta'), nullable=False)
    idTipoPago = db.Column(db.Integer, db.ForeignKey('tipoPagos.idTipoPago'), nullable=False)
    referenciaUnica = db.Column(db.String(50))

    venta = db.relationship('Venta', backref='pagos_venta')
    tipo_pago = db.relationship('TipoPago', backref='pagos_venta')
    
class TipoPago(db.Model):
    __tablename__ = 'tipoPagos'

    idTipoPago = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipoPago = db.Column(db.String(20), nullable=False)
    descripcion = db.Column(db.String(100))

class VentaProducto(db.Model):
    __tablename__ = 'ventaProductos'

    idVentaProducto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idVenta = db.Column(db.Integer, db.ForeignKey('ventas.idVenta'), nullable=False)
    idInventario = db.Column(db.Integer, db.ForeignKey('inventario.idInventario'), nullable=False)
    cantidad = db.Column(db.Float, nullable=False)
    tipoVenta = db.Column(db.String(50), nullable=False)
    precioVenta = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)

    venta = db.relationship('Venta', backref='productos_venta')
    inventario = db.relationship('Inventario', backref='productos_venta')