from models import Usuario, Rol, db

def obtener_usuarios():
    usuarios = db.session.query(
        Usuario.idUsuario,
        Usuario.nombreCompleto,
        Usuario.usuario,
        Rol.nombre,
        Usuario.fechaCreacion
    ).join(
        Rol, Usuario.idRol == Rol.idRol
    ).filter(
        Usuario.estado == True
    ).all()
    
    usuarios_list = []
    for usuario in usuarios:
        usuarios_list.append({
            'idUsuario': usuario.idUsuario,
            'nombreCompleto': usuario.nombreCompleto,
            'usuario': usuario.usuario,
            'rol': usuario.nombre,
            'fechaCreacion': usuario.fechaCreacion
        })
    return usuarios_list

def obtener_usuario(idUsuario):
    usuario = db.session.query(
        Usuario.idUsuario,
        Usuario.nombreCompleto,
        Usuario.usuario,
        Rol.nombre,
        Usuario.fechaCreacion
    ).join(
        Rol, Usuario.idRol == Rol.idRol
    ).filter(
        Usuario.idUsuario == idUsuario
    ).first()
    
    usuario_dict = {
        'idUsuario': usuario.idUsuario,
        'nombreCompleto': usuario.nombreCompleto,
        'usuario': usuario.usuario,
        'rol': usuario.nombre,
        'fechaCreacion': usuario.fechaCreacion
    }
    return usuario_dict

def crear_usuario(nombreCompleto, usuario, contrasena, idRol):
    nuevo_usuario = Usuario(
        nombreCompleto=nombreCompleto,
        usuario=usuario,
        contrasena=contrasena,
        idRol=idRol
    )
    db.session.add(nuevo_usuario)
    db.session.commit()
    return nuevo_usuario.idUsuario

def eliminar_usuario(idUsuario):
    usuario = db.session.query(Usuario).filter(
        Usuario.idUsuario == idUsuario
    ).first()
    usuario.estado = False
    db.session.commit()
    return True

def actualizar_usuario(idUsuario, nombreCompleto, usuario, contrasena, idRol):
    usuario = db.session.query(Usuario).filter(
        Usuario.idUsuario == idUsuario
    ).first()
    usuario.nombreCompleto = nombreCompleto
    usuario.usuario = usuario
    usuario.contrasena = contrasena
    usuario.idRol = idRol
    db.session.commit()
    return True