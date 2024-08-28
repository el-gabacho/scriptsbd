from sqlalchemy import func, case, or_
from sqlalchemy.exc import DBAPIError
from sqlalchemy import or_, and_

from init import db
from inventario.modelos import Inventario, UnidadMedida, Imagenes
from categorias.modelos import Categoria
from vehiculos.modelos import ModeloAutoparte, ModeloAnio, Modelo, Marca, Anio

# OBTENER INFORMACION DE TODOS LOS PRODUTOS ACTIVOS
def get_productos(idMarca, idModelo, anioInicio, anioFin):
    query = db.session.query(
        Inventario.idInventario,
        Inventario.codigoBarras,
        Inventario.nombre,
        Inventario.descripcion,
        Inventario.cantidadActual,
        Inventario.mayoreo,
        Inventario.menudeo,
        Inventario.colocado,
        UnidadMedida.tipoMedida,
        func.coalesce(Categoria.nombre, 'SIN CATEGORIA').label('categoriaNombre'),
        func.coalesce(Imagenes.imgRepresentativa, False).label('imgRepresentativa'),
    ).outerjoin(
        Categoria, Inventario.idCategoria == Categoria.idCategoria
    ).join(
        UnidadMedida, Inventario.idUnidadMedida == UnidadMedida.idUnidadMedida
    ).outerjoin(
        ModeloAutoparte, Inventario.idInventario == ModeloAutoparte.idInventario
    ).outerjoin(
        ModeloAnio, ModeloAutoparte.idModeloAnio == ModeloAnio.idModeloAnio
    ).outerjoin(
        Modelo, ModeloAnio.idModelo == Modelo.idModelo
    ).outerjoin(
        Marca, Modelo.idMarca == Marca.idMarca
    ).outerjoin(
        Anio, ModeloAnio.idAnio == Anio.idAnio
    ).outerjoin(
        Imagenes, Inventario.idInventario == Imagenes.idInventario
    ).filter(
        Inventario.estado == 1,
        Marca.idMarca == idMarca,
        Modelo.idModelo == idModelo,
        Anio.anioInicio == anioInicio,
        Anio.anioFin == anioFin
    ).group_by(
        Inventario.idInventario
    ).all()

    productos_list = []
    for producto in query:
        # Construir la lista de imágenes
        imagen = ""
        if producto.imgRepresentativa:
            imagen = f"{producto.codigoBarras}_1.webp"

        if not imagen:
            imagen = None

        productos_list.append({
            'id': producto.idInventario,
            'codigo': producto.codigoBarras,
            'nombre': producto.nombre,
            'descripcion': producto.descripcion,
            'existencias': producto.cantidadActual,
            'precioMayoreo': producto.mayoreo,
            'precioMenudeo': producto.menudeo,
            'precioColocado': producto.colocado,
            'tipoMedida': producto.tipoMedida,
            'categoria': producto.categoriaNombre,
            'imagen': imagen
        })

    return productos_list

# OBTENER INFORMACION DEL PRODUCTO ACTIVO MEDIANTE SU CODIGO DE BARRAS DE MODO PRECISO ---------------------------------------
def get_producto_preciso(codigo_barras):
    query = db.session.query(
        Inventario.idInventario,
        Inventario.codigoBarras,
        Inventario.nombre,
        Inventario.descripcion,
        Inventario.cantidadActual,
        Inventario.mayoreo,
        Inventario.menudeo,
        Inventario.colocado,
        UnidadMedida.tipoMedida,
        func.coalesce(Categoria.nombre, 'SIN CATEGORIA').label('categoriaNombre'),
        func.group_concat(
            func.concat(
                Marca.nombre, ' ', Modelo.nombre, ' ',
                case(
                    (Anio.anioTodo == 1, 'ALL YEARS'),
                    else_=func.concat(
                        func.right(func.coalesce(Anio.anioInicio, ''), 2),
                        '-',
                        func.right(func.coalesce(Anio.anioFin, ''), 2)
                    )
                )
            ).distinct()
        ).label('aplicaciones'),
        func.coalesce(Imagenes.imgRepresentativa, False).label('imgRepresentativa'),
        func.coalesce(Imagenes.img2, False).label('img2'),
        func.coalesce(Imagenes.img3, False).label('img3'),
        func.coalesce(Imagenes.img4, False).label('img4'),
        func.coalesce(Imagenes.img5, False).label('img5')
    ).outerjoin(
        Categoria, Inventario.idCategoria == Categoria.idCategoria
    ).join(
        UnidadMedida, Inventario.idUnidadMedida == UnidadMedida.idUnidadMedida
    ).outerjoin(
        ModeloAutoparte, Inventario.idInventario == ModeloAutoparte.idInventario
    ).outerjoin(
        ModeloAnio, ModeloAutoparte.idModeloAnio == ModeloAnio.idModeloAnio
    ).outerjoin(
        Modelo, ModeloAnio.idModelo == Modelo.idModelo
    ).outerjoin(
        Marca, Modelo.idMarca == Marca.idMarca
    ).outerjoin(
        Anio, ModeloAnio.idAnio == Anio.idAnio
    ).outerjoin(
        Imagenes, Inventario.idInventario == Imagenes.idInventario
    ).filter(
        Inventario.estado == 1,
        Inventario.codigoBarras == codigo_barras
    ).group_by(
        Inventario.idInventario
    ).first()

    # Procesar el campo de aplicaciones
    aplicaciones = query.aplicaciones
    if aplicaciones:
        aplicaciones = [app.strip() for app in aplicaciones.split(',') if app.strip()]
    else:
        aplicaciones = ["SIN NINGUNA APLICACION"]

    # Construir la lista de imágenes
    imagenes = []
    if query.imgRepresentativa:
        imagenes.append(f"{query.codigoBarras}_1.webp")
    if query.img2:
        imagenes.append(f"{query.codigoBarras}_2.webp")
    if query.img3:
        imagenes.append(f"{query.codigoBarras}_3.webp")
    if query.img4:
        imagenes.append(f"{query.codigoBarras}_4.webp")
    if query.img5:
        imagenes.append(f"{query.codigoBarras}_5.webp")

    producto = {
        'id': query.idInventario,
        'codigo': query.codigoBarras,
        'nombre': query.nombre,
        'descripcion': query.descripcion,
        'existencias': query.cantidadActual,
        'precioMayoreo': query.mayoreo,
        'precioMenudeo': query.menudeo,
        'precioColocado': query.colocado,
        'tipoMedida': query.tipoMedida,
        'categoria': query.categoriaNombre,
        'aplicaciones': aplicaciones,
        'imagenes': imagenes
    }

    return producto

# OBTENER INFORMACION DE PRODUCTOS ACTIVOS MEDIANTE SU buscqueda DE MODO SIMILITUD ---------------------------------------
def get_productos_similares(search_term):
    search_words = search_term.split(" ")

    # Create a reference to the column
    productoCompleto = func.concat(
        Inventario.nombre, ' ', Inventario.descripcion, ' ',
        func.group_concat(func.concat(Marca.nombre, ' ', Modelo.nombre).distinct()).label('productoCompleto')
    )
    
    search_conditions = [productoCompleto.like(f"%{word}%") for word in search_words]

    query = db.session.query(
        Inventario.idInventario,
        Inventario.codigoBarras,
        Inventario.nombre,
        Inventario.descripcion,
        func.coalesce(Categoria.nombre, 'SIN CATEGORIA').label('categoriaNombre'),
        productoCompleto,
        func.coalesce(Imagenes.imgRepresentativa, False).label('imgRepresentativa'),
    ).outerjoin(
        Categoria, Inventario.idCategoria == Categoria.idCategoria
    ).outerjoin(
        ModeloAutoparte, Inventario.idInventario == ModeloAutoparte.idInventario
    ).outerjoin(
        ModeloAnio, ModeloAutoparte.idModeloAnio == ModeloAnio.idModeloAnio
    ).outerjoin(
        Modelo, ModeloAnio.idModelo == Modelo.idModelo
    ).outerjoin(
        Marca, Modelo.idMarca == Marca.idMarca
    ).outerjoin(
        Anio, ModeloAnio.idAnio == Anio.idAnio
    ).outerjoin(
        Imagenes, Inventario.idInventario == Imagenes.idInventario
    ).filter(
        Inventario.estado == 1,
    ).group_by(
        Inventario.idInventario
    ).having(
        and_(*search_conditions)
    ).all()

    productos = []
    for item in query:
        imagen = ""
        if item.imgRepresentativa:
            imagen = f"{item.codigoBarras}_1.webp"

        if not imagen:
            imagen = ''

        productos.append({
            'idInventario': item.idInventario,
            'codigo': item.codigoBarras,
            'nombre': item.nombre,
            'descripcion': item.descripcion,
            'categoria': item.categoriaNombre,
            'imagen': imagen
        })

    return productos