from init import db

class Proveedor(db.Model):
    __tablename__ = 'proveedores'

    idProveedor = db.Column(db.Integer, primary_key=True, autoincrement=True)
    empresa = db.Column(db.String(50), nullable=False)
    nombreEncargado = db.Column(db.String(50))
    telefono = db.Column(db.String(10))
    correo = db.Column(db.String(50))

    proveedor_productos = db.relationship('ProveedorProducto', back_populates='proveedor')