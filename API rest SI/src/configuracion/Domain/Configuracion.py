from models import db

class Configuracion(db.Model):
    __tablename__ = 'configuracion'

    idConfiguracion = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    correo = db.Column(db.String(50))
    direccion = db.Column(db.String(100), nullable=False)
    encabezado = db.Column(db.String(255))
    footer = db.Column(db.String(255))
    

class TelefonosEmpresa(db.Model):
    __tablename__ = 'telefonosEmpresa'

    idTelefono = db.Column(db.Integer, primary_key=True, autoincrement=True)
    numero = db.Column(db.String(20), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)

class Horario(db.Model):
    __tablename__ = 'horario'

    idDia = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dias = db.Column(db.String(50), nullable=False, unique=True)
    horaInicio = db.Column(db.String(10), nullable=False)
    horaFin = db.Column(db.String(10), nullable=False)
