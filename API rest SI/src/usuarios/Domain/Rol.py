from models import db

class Rol(db.Model):
    __tablename__ = 'roles'

    idRol = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.String(100))