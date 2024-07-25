from models import Proveedor

def get_proveedores():
    proveedores = Proveedor.query.all()
    result = []
    for proveedor in proveedores:
        result.append({
            'idProveedor': proveedor.idProveedor,
            'empresa': proveedor.empresa,
            'nombreEncargado': proveedor.nombreEncargado,
            'telefono': proveedor.telefono,
            'correo': proveedor.correo
        })

    return result

def get_proveedor(id):
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