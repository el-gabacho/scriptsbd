from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

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

class Inventario(db.Model):
    __tablename__ = 'inventario'

    idInventario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idCategoria = db.Column(db.Integer, db.ForeignKey('categoria.idCategoria'))  # Asumiendo que existe una tabla `categoria`
    idUnidadMedida = db.Column(db.Integer, db.ForeignKey('unidadmedidas.idUnidadMedida'))
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
    proveedor_productos = db.relationship('ProveedorProducto', backref='inventarios')
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
    __tablename__ = 'unidadmedidas'

    idUnidadMedida = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipoMedida = db.Column(db.String(8), unique=True, nullable=False)
    descripcion = db.Column(db.String(100))

class ProveedorProducto(db.Model):
    __tablename__ = 'proveedorproductos'

    idProveedorProducto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idProveedor = db.Column(db.Integer, db.ForeignKey('proveedores.idProveedor'), nullable=False)
    idInventario = db.Column(db.Integer, db.ForeignKey('inventario.idInventario'), nullable=False)

    proveedor = db.relationship('Proveedor', backref='productos_proveedor')
    inventario = db.relationship('Inventario', backref='productos_inventario')

class Rol(db.Model):
    __tablename__ = 'roles'

    idRol = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.String(100))

class Modelo(db.Model):
    __tablename__ = 'modelos'

    idModelo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idMarca = db.Column(db.Integer, db.ForeignKey('marcas.idMarca'), nullable=False)
    nombre = db.Column(db.String(50), nullable=False)

    marca = db.relationship('Marca', backref='modelos')

class Anio(db.Model):
    __tablename__ = 'anios'

    idAnio = db.Column(db.Integer, primary_key=True, autoincrement=True)
    anioInicio = db.Column(db.Integer, nullable=False)
    anioFin = db.Column(db.Integer, nullable=False)
    anioTodo = db.Column(db.Boolean, default=False, nullable=False)

    __table_args__ = (db.UniqueConstraint('anioInicio', 'anioFin'),)

class ModeloAnio(db.Model):
    __tablename__ = 'modeloAnios'

    idModeloAnio = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idModelo = db.Column(db.Integer, db.ForeignKey('modelos.idModelo'), nullable=False)
    idAnio = db.Column(db.Integer, db.ForeignKey('anios.idAnio'), nullable=False)

    modelo = db.relationship('Modelo', backref='modeloAnios')
    anio = db.relationship('Anio', backref='modeloAnios')

class ModeloAutoparte(db.Model):
    __tablename__ = 'modeloAutopartes'

    idModeloAutoparte = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idModeloAnio = db.Column(db.Integer, db.ForeignKey('modeloAnios.idModeloAnio'), nullable=False)
    idInventario = db.Column(db.Integer, db.ForeignKey('inventario.idInventario'), nullable=False)

    modeloAnio = db.relationship('ModeloAnio', backref='modeloAutopartes')
    inventario = db.relationship('Inventario', backref='modeloAutopartes')

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
    
class Cliente(db.Model):
    __tablename__ = 'clientes'

    idCliente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(30), nullable=False)