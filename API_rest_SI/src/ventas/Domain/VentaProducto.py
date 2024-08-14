from init import db

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