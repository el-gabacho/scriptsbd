from models import db

class Modelo(db.Model):
    __tablename__ = 'modelos'

    idModelo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idMarca = db.Column(db.Integer, db.ForeignKey('marcas.idMarca'), nullable=False)
    nombre = db.Column(db.String(50), nullable=False)

    marca = db.relationship('Marca', backref='modelos')