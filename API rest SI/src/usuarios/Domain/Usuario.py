from itsdangerous import URLSafeTimedSerializer as Serializer
from werkzeug.security import check_password_hash
from models import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    idUsuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idRol = db.Column(db.Integer, db.ForeignKey('roles.idRol'), nullable=False)
    nombreCompleto = db.Column(db.String(50), nullable=False)
    usuario = db.Column(db.String(15), nullable=False)
    contrasenia = db.Column(db.String(100), nullable=False)
    fechaCreacion = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    estado = db.Column(db.Boolean, default=True)

    rol = db.relationship('Rol', backref='usuarios')
    
    def check_password(self, password):
        return check_password_hash(self.contrasenia, password)
    
    def generate_token(self, secret_key):
        s = Serializer(secret_key)
        return s.dumps({'user_id': self.idUsuario})