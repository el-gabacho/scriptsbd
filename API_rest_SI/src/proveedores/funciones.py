from proveedores.modelos import db, Proveedor

def obtener_proveedores():
    proveedores = Proveedor.query.all()
    result = []
    for proveedor in proveedores:
        result.append({
            'Id': proveedor.idProveedor,
            'Nombre': proveedor.empresa,
            'Encargado': proveedor.nombreEncargado,
            'Telefono': proveedor.telefono,
            'Correo': proveedor.correo
        })

    return result

def obtener_proveedor(id):
    proveedor = Proveedor.query.get(id)
    if proveedor:
        result = {
            'idProveedor': proveedor.idProveedor,
            'empresa': proveedor.empresa,
            'nombreEncargado': proveedor.nombreEncargado,
            'telefono': proveedor.telefono,
            'correo': proveedor.correo
        }
        return result
    
def crear_proveedor(empresa, nombreEncargado, telefono, correo):
    proveedor_existente = Proveedor.query.filter(Proveedor.empresa.ilike(empresa)).first()
    if proveedor_existente:
        raise ValueError(f'No se puede crear el proveedor "{empresa}" porque ya existe.')
    
    nuevo_proveedor = Proveedor(
        empresa=empresa,
        nombreEncargado=nombreEncargado,
        telefono=telefono,
        correo=correo
    )
    db.session.add(nuevo_proveedor)
    db.session.commit()
    return nuevo_proveedor.idProveedor

def eliminar_proveedor(idProveedor):
    proveedor = Proveedor.query.get(idProveedor)

    # Eliminar los productos del proveedor
    for producto in proveedor.proveedor_productos:
        db.session.delete(producto)

    # Ahora puedes eliminar el proveedor
    db.session.delete(proveedor)
    db.session.commit()
    return True

def actualizar_proveedor(idProveedor, empresa, nombreEncargado, telefono, correo):
    proveedor = Proveedor.query.get(idProveedor)
    if not proveedor:
        raise ValueError(f'No se encontró el proveedor con ID {idProveedor}.')
    
    proveedor_existente = Proveedor.query.filter(Proveedor.empresa.ilike(empresa)).first()
    if proveedor_existente and proveedor_existente.idProveedor != idProveedor:
        raise ValueError(f'Ya existe un proveedor con el nombre "{empresa}".')
    
    if proveedor.empresa == empresa:
        return 'sin_cambio'
    
    proveedor.empresa = empresa
    proveedor.nombreEncargado = nombreEncargado
    proveedor.telefono = telefono
    proveedor.correo = correo
    db.session.commit()
    return True

def obtener_id_proveedor(proveedor):
    resultado = db.session.query(
        Proveedor.idProveedor
    ).filter(
        Proveedor.empresa == proveedor
    ).first()
    return resultado[0] if resultado else None