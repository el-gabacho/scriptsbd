from flask_sqlalchemy import SQLAlchemy
from models import db

class Categoria(db.Model):
    __tablename__ = 'categorias'

    idCategoria = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)