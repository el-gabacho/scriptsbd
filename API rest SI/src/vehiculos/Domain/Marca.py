from models import db, ma

class Marca(db.Model):
    __tablename__ = 'marcas'
    
    idMarca = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(45), unique=True, nullable=False)
    urlLogo = db.Column(db.String(300), nullable=True)

    def __init__(self, nombre, urlLogo=None):
        self.nombre = nombre
        self.urlLogo = urlLogo

class MarcaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Marca
        load_instance = True