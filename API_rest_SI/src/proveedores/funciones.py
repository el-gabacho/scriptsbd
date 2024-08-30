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
    db.session.delete(proveedor)
    db.session.commit()
    return True

def actualizar_proveedor(idProveedor, empresa, nombreEncargado, telefono, correo):
    proveedor = Proveedor.query.get(idProveedor)
    proveedor.empresa = empresa
    proveedor.nombreEncargado = nombreEncargado
    proveedor.telefono = telefono
    proveedor.correo = correo
    db.session.commit()
    return True