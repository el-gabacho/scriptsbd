from werkzeug.security import generate_password_hash
from usuarios.modelos import db, Usuario, Rol

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
            'Id': usuario.idUsuario,
            'NombreCompleto': usuario.nombreCompleto,
            'NombreUsuario': usuario.usuario,
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

def crear_usuario(nombre, username, password, idRol):
    usuario_existente = Usuario.query.filter(Usuario.usuario.ilike(username)).first()
    if usuario_existente:
        raise ValueError(f'No se puede crear el usuario "{username}" porque ya existe.')
    
    password_hash = generate_password_hash(password)
    nuevo_usuario = Usuario(
        nombreCompleto=nombre,
        usuario=username,
        contrasenia=password_hash,
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

def actualizar_usuario(idUsuario, nombreCompleto, username, password, idRol, fechaCreacion):
    usuario = db.session.query(Usuario).filter(
        Usuario.idUsuario == idUsuario
    ).first()
    if not usuario:
        raise ValueError(f'No se encontró el usuario con ID {idUsuario}.')
    
    usuario_existente = Usuario.query.filter(Usuario.usuario.ilike(username)).first()
    if usuario_existente and usuario_existente.idUsuario != idUsuario:
        raise ValueError(f'Ya existe un usuario con el nombre de usuario "{username}".')
    
    if usuario.usuario == username:
        return 'sin_cambio'
    
    password_hash = generate_password_hash(password)
    usuario.nombreCompleto = nombreCompleto
    usuario.usuario = username
    usuario.contrasenia = password_hash
    usuario.idRol = idRol
    usuario.fechaCreacion = fechaCreacion
    
    db.session.commit()
    return True