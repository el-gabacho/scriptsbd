from init import db

class Inventario(db.Model):
    __tablename__ = 'inventario'

    idInventario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idCategoria = db.Column(db.Integer, db.ForeignKey('categoria.idCategoria'))  # Asumiendo que existe una tabla `categoria`
    idUnidadMedida = db.Column(db.Integer, db.ForeignKey('unidadMedidas.idUnidadMedida'))
    codigoBarras = db.Column(db.String(50), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(150), nullable=False)
    cantidadActual = db.Column(db.Float, nullable=False, default=0.0)
    cantidadMinima = db.Column(db.Float, nullable=False, default=1.0)
    precioCompra = db.Column(db.Float, nullable=False, default=0.0)
    mayoreo = db.Column(db.Float, nullable=False, default=0.0)
    menudeo = db.Column(db.Float, nullable=False, default=0.0)
    colocado = db.Column(db.Float, nullable=False, default=0.0)
    estado = db.Column(db.Boolean, nullable=False, default=1)

    unidad_medida = db.relationship('UnidadMedida', backref='inventarios')
    imagenes = db.relationship('Imagenes', backref='inventarios')

class Imagenes(db.Model):
    __tablename__ = 'imagenes'

    idImagenes = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idInventario = db.Column(db.Integer, db.ForeignKey('inventario.idInventario'))
    imgRepresentativa = db.Column(db.Boolean, nullable=False, default=False)
    img2 = db.Column(db.Boolean, nullable=False, default=False)
    img3 = db.Column(db.Boolean, nullable=False, default=False)
    img4 = db.Column(db.Boolean, nullable=False, default=False)
    img5 = db.Column(db.Boolean, nullable=False, default=False)

class UnidadMedida(db.Model):
    __tablename__ = 'unidadMedidas'

    idUnidadMedida = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipoMedida = db.Column(db.String(8), unique=True, nullable=False)
    descripcion = db.Column(db.String(100))