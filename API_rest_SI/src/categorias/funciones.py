from categorias.modelos import db, Categoria

def obtener_categorias():
    from inventario.modelos import Inventario
    categorias = Categoria.query \
        .join(Inventario, Categoria.idCategoria == Inventario.idCategoria, isouter=True) \
        .with_entities(Categoria.idCategoria, Categoria.nombre, db.func.count(Inventario.idInventario).label('numProductos')) \
        .group_by(Categoria.idCategoria, Categoria.nombre) \
        .order_by(Categoria.idCategoria) \
        .all()

    result = []
    for categoria in categorias:
        result.append({
            'Id': categoria.idCategoria,
            'Nombre': categoria.nombre,
            'NumProductos': categoria.numProductos
        })

    return result

def crear_categoria(nombre):
    nueva_categoria = Categoria(nombre=nombre)
    db.session.add(nueva_categoria)
    db.session.commit()
    return nueva_categoria.idCategoria

def eliminar_categoria(idCategoria):
    categoria = Categoria.query.get(idCategoria)
    db.session.delete(categoria)
    db.session.commit()
    return True

def actualizar_categoria(idCategoria, nombre):
    categoria = Categoria.query.get(idCategoria)
    categoria.nombre = nombre
    db.session.commit()
    return True

def obtener_id_categoria(categoria):
    resultado = db.session.query(
        Categoria.idCategoria
    ).filter(
        Categoria.nombre == categoria
    ).first()
    return resultado[0] if resultado else None