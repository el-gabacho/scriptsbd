from models import db

class Cliente(db.Model):
    __tablename__ = 'clientes'

    idCliente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(30), nullable=False)