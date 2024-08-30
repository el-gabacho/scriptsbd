from init import db, ma

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
        
class Modelo(db.Model):
    __tablename__ = 'modelos'

    idModelo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idMarca = db.Column(db.Integer, db.ForeignKey('marcas.idMarca'), nullable=False)
    nombre = db.Column(db.String(50), nullable=False)

    marca = db.relationship('Marca', backref='modelos')
    
class ModeloAutoparte(db.Model):
    __tablename__ = 'modeloAutopartes'

    idModeloAutoparte = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idModeloAnio = db.Column(db.Integer, db.ForeignKey('modeloAnios.idModeloAnio'), nullable=False)
    idInventario = db.Column(db.Integer, db.ForeignKey('inventario.idInventario'), nullable=False)

    modeloAnio = db.relationship('ModeloAnio', backref='modeloAutopartes')
    inventario = db.relationship('Inventario', backref='modeloAutopartes')
    
class ModeloAnio(db.Model):
    __tablename__ = 'modeloAnios'

    idModeloAnio = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idModelo = db.Column(db.Integer, db.ForeignKey('modelos.idModelo'), nullable=False)
    idAnio = db.Column(db.Integer, db.ForeignKey('anios.idAnio'), nullable=False)

    modelo = db.relationship('Modelo', backref='modeloAnios')
    anio = db.relationship('Anio', backref='modeloAnios')
    
class Anio(db.Model):
    __tablename__ = 'anios'

    idAnio = db.Column(db.Integer, primary_key=True, autoincrement=True)
    anioInicio = db.Column(db.Integer, nullable=False)
    anioFin = db.Column(db.Integer, nullable=False)
    anioTodo = db.Column(db.Boolean, default=False, nullable=False)

    __table_args__ = (db.UniqueConstraint('anioInicio', 'anioFin'),)