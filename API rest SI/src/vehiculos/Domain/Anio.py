from init import db

class Anio(db.Model):
    __tablename__ = 'anios'

    idAnio = db.Column(db.Integer, primary_key=True, autoincrement=True)
    anioInicio = db.Column(db.Integer, nullable=False)
    anioFin = db.Column(db.Integer, nullable=False)
    anioTodo = db.Column(db.Boolean, default=False, nullable=False)

    __table_args__ = (db.UniqueConstraint('anioInicio', 'anioFin'),)