from flask import request, jsonify
from categorias.modelos import db, Categoria
from sqlalchemy import func

def obtener_categorias():
    from inventario.modelos import Inventario

    # Consulta con outer join para obtener las categorías y la cantidad de productos
    categorias = Categoria.query \
        .join(Inventario, Categoria.idCategoria == Inventario.idCategoria, isouter=True) \
        .with_entities(
            Categoria.idCategoria, 
            Categoria.nombre, 
            db.func.count(Inventario.idInventario).label('numProductos')
        ) \
        .group_by(Categoria.idCategoria, Categoria.nombre) \
        .order_by(Categoria.idCategoria) \
        .all()

    # Convertimos los resultados en una lista de diccionarios
    result = [
        {
            'Id': categoria.idCategoria,
            'Nombre': categoria.nombre,
            'NumProductos': categoria.numProductos
        }
        for categoria in categorias
    ]

    return result

# -----------------------------------------------------------------------------------------------------------------------

def crear_categoria(nombre_categoria):
    # Verificar si la categoría ya existe
    categoria_existente = Categoria.query.filter(Categoria.nombre.ilike(nombre_categoria)).first()
    if categoria_existente:
        # Lanza un ValueError que será manejado en el nivel superior
        raise ValueError(f'No se puede crear la categoría "{nombre_categoria}" porque ya existe.')

    # Crear nueva categoría
    nueva_categoria = Categoria(nombre=nombre_categoria)
    db.session.add(nueva_categoria)
    db.session.commit()

    return nueva_categoria.idCategoria

# -----------------------------------------------------------------------------------------------------------------------

def actualizar_categoria(idCategoria, nombre):
    categoria = Categoria.query.get(idCategoria)
    if not categoria:
        raise ValueError(f'No se encontró la categoría con ID {idCategoria}.')
    
    # Verificar si la categoría con el nuevo nombre ya existe
    categoria_existente = Categoria.query.filter(Categoria.nombre.ilike(nombre)).first()
    if categoria_existente and categoria_existente.idCategoria != idCategoria:
        raise ValueError(f'Ya existe una categoría con el nombre "{nombre}".')
    
    # Verificar si el nombre es el mismo que el actual
    if categoria.nombre == nombre:
        return 'sin_cambio'
    
    # Actualizar la categoría
    categoria.nombre = nombre
    db.session.commit()
    return True

# -----------------------------------------------------------------------------------------------------------------------

def eliminar_categoria(idCategoria):
    from inventario.modelos import Inventario
    categoria = Categoria.query.get(idCategoria)

    if not categoria:
        return 'no_encontrado'

    # Verificar si hay productos asociados a la categoría
    productos_asociados = Inventario.query.filter_by(idCategoria=idCategoria).count()

    if productos_asociados > 0:
        return 'productos_asociados'
    
    db.session.delete(categoria)
    db.session.commit()
    return True

# -----------------------------------------------------------------------------------------------------------------------

def obtener_id_categoria(categoria):
    resultado = db.session.query(
        Categoria.idCategoria
    ).filter(
        Categoria.nombre == categoria
    ).first()
    return resultado[0] if resultado else None

# -----------------------------------------------------------------------------------------------------------------------

# OBTENER INFORMACION DE CATEGORIAS CON SIMILITUD EN EL NOMBRE -------------------------------------------
def obtener_categorias_similares(nombre_categoria):
    from inventario.modelos import Inventario
    query = db.session.query(
        Categoria.idCategoria,
        Categoria.nombre,
        func.count(Inventario.idInventario).label('numProductos')
    ).outerjoin(
        Inventario, Categoria.idCategoria == Inventario.idCategoria
    ).filter(
        Categoria.nombre.ilike(f'%{nombre_categoria}%')  # Buscar coincidencias parciales
    ).group_by(
        Categoria.idCategoria,
        Categoria.nombre
    ).order_by(
        Categoria.idCategoria
    ).all()

    categorias = []
    for item in query:
        categorias.append({
            'Id': item.idCategoria,
            'Nombre': item.nombre,
            'NumProductos': item.numProductos
        })

    return categorias