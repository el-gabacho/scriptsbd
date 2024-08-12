from models import db

class ModeloAnio(db.Model):
    __tablename__ = 'modeloAnios'

    idModeloAnio = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idModelo = db.Column(db.Integer, db.ForeignKey('modelos.idModelo'), nullable=False)
    idAnio = db.Column(db.Integer, db.ForeignKey('anios.idAnio'), nullable=False)

    modelo = db.relationship('Modelo', backref='modeloAnios')
    anio = db.relationship('Anio', backref='modeloAnios')