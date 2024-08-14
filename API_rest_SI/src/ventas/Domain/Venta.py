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