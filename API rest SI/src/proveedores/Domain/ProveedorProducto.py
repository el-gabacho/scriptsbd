from models import db

class ProveedorProducto(db.Model):
    __tablename__ = 'proveedorproductos'

    idProveedorProducto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idProveedor = db.Column(db.Integer, db.ForeignKey('proveedores.idProveedor'), nullable=False)
    idInventario = db.Column(db.Integer, db.ForeignKey('inventario.idInventario'), nullable=False)

    proveedor = db.relationship('Proveedor', backref='productos_proveedor')
    inventario = db.relationship('Inventario', backref='productos_inventario')