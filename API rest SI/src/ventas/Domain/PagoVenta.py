from init import db

class PagoVenta(db.Model):
    __tablename__ = 'pagoVenta'

    idPagoVenta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idVenta = db.Column(db.Integer, db.ForeignKey('ventas.idVenta'), nullable=False)
    idTipoPago = db.Column(db.Integer, db.ForeignKey('tipoPagos.idTipoPago'), nullable=False)
    referenciaUnica = db.Column(db.String(50))

    venta = db.relationship('Venta', backref='pagos_venta')
    tipo_pago = db.relationship('TipoPago', backref='pagos_venta')