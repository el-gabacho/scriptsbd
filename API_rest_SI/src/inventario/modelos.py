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
    proveedor_productos = db.relationship('ProveedorProducto', back_populates='inventario', overlaps="inventarios,proveedor_productos")
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
    
class EntradaProducto(db.Model):
    __tablename__ = 'entradaProductos'

    idEntradaProducto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idUsuario = db.Column(db.Integer, db.ForeignKey('usuarios.idUsuario'), nullable=False)
    idInventario = db.Column(db.Integer, db.ForeignKey('inventario.idInventario'), nullable=False)
    cantidadNueva = db.Column(db.Float, nullable=False)
    precioCompra = db.Column(db.Float, nullable=False)
    fechaEntrada = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())

    usuario = db.relationship('Usuario', backref='entradas_productos')
    inventario = db.relationship('Inventario', backref='entradas_productos')
    
class RegistroProducto(db.Model):
    __tablename__ = 'registroProductos'

    idRegistroProducto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idInventario = db.Column(db.Integer, db.ForeignKey('inventario.idInventario'), nullable=False)
    idUsuarioRegistro = db.Column(db.Integer, db.ForeignKey('usuarios.idUsuario'), nullable=False)
    fechaCreacion = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    idUsuarioElimino = db.Column(db.Integer, db.ForeignKey('usuarios.idUsuario'), default=None)
    fechaElimino = db.Column(db.TIMESTAMP, default=None)

    inventario = db.relationship('Inventario', backref='registros_productos')
    usuario_registro = db.relationship('Usuario', foreign_keys=[idUsuarioRegistro], backref='registros_productos')
    usuario_elimino = db.relationship('Usuario', foreign_keys=[idUsuarioElimino], backref='registros_productos_deleted')