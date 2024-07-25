from models import db, Categoria, Inventario

def get_categorias():
    categorias = Categoria.query \
        .join(Inventario, Categoria.idCategoria == Inventario.idCategoria, isouter=True) \
        .with_entities(Categoria.idCategoria, Categoria.nombre, db.func.count(Inventario.idInventario).label('numProductos')) \
        .group_by(Categoria.idCategoria, Categoria.nombre) \
        .order_by(Categoria.idCategoria) \
        .all()

    result = []
    for categoria in categorias:
        result.append({
            'idCategoria': categoria.idCategoria,
            'nombre': categoria.nombre,
            'numProductos': categoria.numProductos
        })

    return result