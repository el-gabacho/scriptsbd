from init import db

class ProveedorProducto(db.Model):
    __tablename__ = 'proveedorProductos'

    idProveedorProducto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idProveedor = db.Column(db.Integer, db.ForeignKey('proveedores.idProveedor'), nullable=False)
    idInventario = db.Column(db.Integer, db.ForeignKey('inventario.idInventario'), nullable=False)

    proveedor = db.relationship('Proveedor', back_populates='proveedor_productos')
    inventario = db.relationship('Inventario', back_populates='proveedor_productos', overlaps="inventarios,proveedor_productos")