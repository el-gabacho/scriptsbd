from init import db

class ModeloAutoparte(db.Model):
    __tablename__ = 'modeloAutopartes'

    idModeloAutoparte = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idModeloAnio = db.Column(db.Integer, db.ForeignKey('modeloAnios.idModeloAnio'), nullable=False)
    idInventario = db.Column(db.Integer, db.ForeignKey('inventario.idInventario'), nullable=False)

    modeloAnio = db.relationship('ModeloAnio', backref='modeloAutopartes')
    inventario = db.relationship('Inventario', backref='modeloAutopartes')