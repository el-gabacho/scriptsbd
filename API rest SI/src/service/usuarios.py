from models import Usuario, Rol, db

def get_usuarios():
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