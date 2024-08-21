from categorias.modelos import db, Categoria
from inventario.modelos import Inventario

def obtener_categorias():
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