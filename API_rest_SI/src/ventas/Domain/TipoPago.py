from init import db

class TipoPago(db.Model):
    __tablename__ = 'tipoPagos'

    idTipoPago = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipoPago = db.Column(db.String(20), nullable=False)
    descripcion = db.Column(db.String(100))