from sqlalchemy import func, case, or_, text, and_
from sqlalchemy.exc import DBAPIError, SQLAlchemyError
from init import db
from inventario.modelos import Inventario, UnidadMedida, Imagenes
from categorias.modelos import Categoria
from proveedores.modelos import Proveedor, ProveedorProducto
from vehiculos.modelos import Marca, ModeloAutoparte, ModeloAnio, Modelo, Anio
import os
from config import IMAGE_ROOT_PATH

# OBTENER INFORMACION DE TODOS LOS PRODUTOS ACTIVOS
def get_productos():
    query = db.session.query(
        Inventario.idInventario,
        Inventario.codigoBarras,
        Inventario.nombre,
        Inventario.descripcion,
        Inventario.cantidadActual,
        Inventario.cantidadMinima,
        Inventario.precioCompra,
        Inventario.mayoreo,
        Inventario.menudeo,
        Inventario.colocado,
        Inventario.estado,
        UnidadMedida.tipoMedida,
        func.coalesce(Categoria.nombre, 'SIN CATEGORIA').label('categoriaNombre'),
        func.coalesce(Proveedor.empresa, 'SIN PROVEEDOR').label('proveedorEmpresa'),
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
        ProveedorProducto, Inventario.idInventario == ProveedorProducto.idInventario
    ).outerjoin(
        Proveedor, ProveedorProducto.idProveedor == Proveedor.idProveedor
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
        Inventario.estado == 1
    ).group_by(
        Inventario.idInventario
    ).limit(100).all()

    productos_list = []
    for producto in query:
        aplicaciones = producto.aplicaciones
        if not aplicaciones:
            aplicaciones = ["SIN NINGUNA APLICACION"]
        else:
            aplicaciones = [app.strip() for app in aplicaciones.split(',') if app.strip()]

        # Construir la lista de imágenes
        imagenes_str = f"{producto.imgRepresentativa},{producto.img2},{producto.img3},{producto.img4},{producto.img5}"

        productos_list.append({
            'IdInventario': producto.idInventario,
            'Codigo': producto.codigoBarras,
            'Nombre': producto.nombre,
            'Descripcion': producto.descripcion,
            'Existencias': producto.cantidadActual,
            'CantidadMinima': producto.cantidadMinima,
            'PrecioCompra': producto.precioCompra,
            'PrecioMayoreo': producto.mayoreo,
            'PrecioMenudeo': producto.menudeo,
            'PrecioColocado': producto.colocado,
            'TipoMedida': producto.tipoMedida,
            'Proveedor': producto.proveedorEmpresa,
            'Categoria': producto.categoriaNombre,
            'Aplicaciones': aplicaciones,
            'Imagenes': imagenes_str
        })

    return productos_list

# OBTENER INFORMACION DEL PRODUCTO ACTIVO MEDIANTE SU CODIGO DE BARRAS DE MODO PRECISO ---------------------------------------
def get_producto_preciso(codigo_barras):
    # Ejecutar la consulta
    query = db.session.query(
        Inventario.idInventario,
        Inventario.codigoBarras,
        Inventario.nombre,
        Inventario.descripcion,
        Inventario.cantidadActual,
        Inventario.cantidadMinima,
        Inventario.precioCompra,
        Inventario.mayoreo,
        Inventario.menudeo,
        Inventario.colocado,
        Inventario.estado,
        UnidadMedida.tipoMedida,
        func.coalesce(Categoria.nombre, 'SIN CATEGORIA').label('categoriaNombre'),
        func.coalesce(Proveedor.empresa, 'SIN PROVEEDOR').label('proveedorEmpresa'),
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
        ProveedorProducto, Inventario.idInventario == ProveedorProducto.idInventario
    ).outerjoin(
        Proveedor, ProveedorProducto.idProveedor == Proveedor.idProveedor
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
    ).first()

    # Validar que la consulta no sea None
    if query.idInventario is None:
        return None

    # Procesar el campo de aplicaciones
    aplicaciones = query.aplicaciones
    if aplicaciones:
        aplicaciones = [app.strip() for app in aplicaciones.split(',') if app.strip()]
    else:
        aplicaciones = ["SIN NINGUNA APLICACION"]

    # Construir la lista de imágenes
    imagenes_str = f"{query.imgRepresentativa},{query.img2},{query.img3},{query.img4},{query.img5}"

    producto = {
        'IdInventario': query.idInventario,
        'Codigo': query.codigoBarras,
        'Nombre': query.nombre,
        'Descripcion': query.descripcion,
        'Existencias': query.cantidadActual,
        'CantidadMinima': query.cantidadMinima,
        'PrecioCompra': query.precioCompra,
        'PrecioMayoreo': query.mayoreo,
        'PrecioMenudeo': query.menudeo,
        'PrecioColocado': query.colocado,
        'TipoMedida': query.tipoMedida,
        'Proveedor': query.proveedorEmpresa,
        'Categoria': query.categoriaNombre,
        'Aplicaciones': aplicaciones,
        'Imagenes': imagenes_str
    }

    return producto

def obtener_producto_preciso_incluyendo_eliminados(codigo_barras):
    query = db.session.query(
        Inventario.idInventario,
        Inventario.codigoBarras,
        Inventario.nombre,
        Inventario.descripcion,
        Inventario.cantidadActual,
        Inventario.cantidadMinima,
        Inventario.precioCompra,
        Inventario.mayoreo,
        Inventario.menudeo,
        Inventario.colocado,
        Inventario.estado,
        UnidadMedida.tipoMedida,
        func.coalesce(Categoria.nombre, 'SIN CATEGORIA').label('categoriaNombre'),
        func.coalesce(Proveedor.empresa, 'SIN PROVEEDOR').label('proveedorEmpresa'),
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
        ProveedorProducto, Inventario.idInventario == ProveedorProducto.idInventario
    ).outerjoin(
        Proveedor, ProveedorProducto.idProveedor == Proveedor.idProveedor
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
        Inventario.codigoBarras == codigo_barras
    ).first()

    # Validar que la consulta no sea None
    if query.idInventario is None:
        return None

    # Procesar el campo de aplicaciones
    aplicaciones = query.aplicaciones
    if aplicaciones:
        aplicaciones = [app.strip() for app in aplicaciones.split(',') if app.strip()]
    else:
        aplicaciones = ["SIN NINGUNA APLICACION"]

    # Construir la lista de imágenes
    imagenes_str = f"{query.imgRepresentativa},{query.img2},{query.img3},{query.img4},{query.img5}"

    producto = {
        'IdInventario': query.idInventario,
        'Codigo': query.codigoBarras,
        'Nombre': query.nombre,
        'Descripcion': query.descripcion,
        'Existencias': query.cantidadActual,
        'CantidadMinima': query.cantidadMinima,
        'PrecioCompra': query.precioCompra,
        'PrecioMayoreo': query.mayoreo,
        'PrecioMenudeo': query.menudeo,
        'PrecioColocado': query.colocado,
        'TipoMedida': query.tipoMedida,
        'Proveedor': query.proveedorEmpresa,
        'Categoria': query.categoriaNombre,
        'Aplicaciones': aplicaciones,
        'Imagenes': imagenes_str
    }

    return producto
# OBTENER INFORMACION DE PRODUCTOS ACTIVOS MEDIANTE SU CODIGO DE BARRAS DE MODO SIMILITUD ---------------------------------------
def get_productos_similares(codigo_barras):
    query = db.session.query(
        Inventario.idInventario,
        Inventario.codigoBarras,
        Inventario.nombre,
        Inventario.descripcion,
        Inventario.cantidadActual,
        Inventario.cantidadMinima,
        Inventario.precioCompra,
        Inventario.mayoreo,
        Inventario.menudeo,
        Inventario.colocado,
        Inventario.estado,
        UnidadMedida.tipoMedida,
        func.coalesce(Categoria.nombre, 'SIN CATEGORIA').label('categoriaNombre'),
        func.coalesce(Proveedor.empresa, 'SIN PROVEEDOR').label('proveedorEmpresa'),
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
        ProveedorProducto, Inventario.idInventario == ProveedorProducto.idInventario
    ).outerjoin(
        Proveedor, ProveedorProducto.idProveedor == Proveedor.idProveedor
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
        Inventario.codigoBarras.like(f'%{codigo_barras}%')  # Buscar coincidencias parciales
    ).group_by(
        Inventario.idInventario
    ).limit(100).all()

    productos = []
    for item in query:
        aplicaciones = item.aplicaciones
        if aplicaciones:
            aplicaciones = [app.strip() for app in aplicaciones.split(',') if app.strip()]
        else:
            aplicaciones = ["SIN NINGUNA APLICACION"]

        imagenes_str = f"{item.imgRepresentativa},{item.img2},{item.img3},{item.img4},{item.img5}"

        productos.append({
            'IdInventario': item.idInventario,
            'Codigo': item.codigoBarras,
            'Nombre': item.nombre,
            'Descripcion': item.descripcion,
            'Existencias': item.cantidadActual,
            'CantidadMinima': item.cantidadMinima,
            'PrecioCompra': item.precioCompra,
            'PrecioMayoreo': item.mayoreo,
            'PrecioMenudeo': item.menudeo,
            'PrecioColocado': item.colocado,
            'TipoMedida': item.tipoMedida,
            'Proveedor': item.proveedorEmpresa,
            'Categoria': item.categoriaNombre,
            'Aplicaciones': aplicaciones,
            'Imagenes': imagenes_str
        })

    return productos

# OBTENER INFORMACION DE PRODUCTOS ACTIVOS MEDIANTE DICHA INFORMACION DE MODO SIMILITUD MUCHOS PARAMETROS
def get_productos_avanzada(filtros):
    query = db.session.query(
        Inventario.idInventario,
        Inventario.codigoBarras,
        Inventario.nombre,
        Inventario.descripcion,
        Inventario.cantidadActual,
        Inventario.cantidadMinima,
        Inventario.precioCompra,
        Inventario.mayoreo,
        Inventario.menudeo,
        Inventario.colocado,
        Inventario.estado,
        UnidadMedida.tipoMedida,
        func.coalesce(Categoria.nombre, 'SIN CATEGORIA').label('categoriaNombre'),
        func.coalesce(Proveedor.empresa, 'SIN PROVEEDOR').label('proveedorEmpresa'),
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
        ).label('aplicaciones')
    ).outerjoin(
        Categoria, Inventario.idCategoria == Categoria.idCategoria
    ).join(
        UnidadMedida, Inventario.idUnidadMedida == UnidadMedida.idUnidadMedida
    ).outerjoin(
        ProveedorProducto, Inventario.idInventario == ProveedorProducto.idInventario
    ).outerjoin(
        Proveedor, ProveedorProducto.idProveedor == Proveedor.idProveedor
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
    ).filter(
        Inventario.estado == 1
    )
    
    # Aplicar filtros si existen
    if filtros.get('codigo'):
        query = query.filter(Inventario.codigoBarras.like(f"%{filtros['codigo']}%"))
    if filtros.get('nombre'):
        query = query.filter(Inventario.nombre.like(f"%{filtros['nombre']}%"))
    if filtros.get('descripcion'):
        query = query.filter(Inventario.descripcion.like(f"%{filtros['descripcion']}%"))
    if filtros.get('categoria'):
        query = query.filter(Categoria.nombre.like(f"%{filtros['categoria']}%"))
    if filtros.get('proveedor'):
        query = query.filter(Proveedor.empresa.like(f"%{filtros['proveedor']}%"))
    if filtros.get('marca'):
        query = query.filter(Marca.nombre.like(f"%{filtros['marca']}%"))
    if filtros.get('modelo'):
        query = query.filter(Modelo.nombre.like(f"%{filtros['modelo']}%"))
    
    # Filtros por fecha y booleano
    if filtros.get('fecha_inicio') and filtros.get('fecha_fin'):
        fecha_inicio = filtros['fecha_inicio']
        fecha_fin = filtros['fecha_fin']
        try:
            fecha_inicio = int(fecha_inicio)
            fecha_fin = int(fecha_fin)
            query = query.filter(
                and_(
                    Anio.anioInicio >= fecha_inicio,
                    Anio.anioFin <= fecha_fin
                )
            )
        except ValueError:
            pass  # Manejar el caso en que las fechas no son válidas

    if filtros.get('anio_todo') is not None:
        query = query.filter(Anio.anioTodo == filtros['anio_todo'])
    
    query = query.group_by(
        Inventario.idInventario
    ).limit(100).all()

    productos = []
    for item in query:
        aplicaciones = item.aplicaciones
        if aplicaciones:
            aplicaciones = [app.strip() for app in aplicaciones.split(',') if app.strip()]
        else:
            aplicaciones = ["SIN NINGUNA APLICACION"]

        productos.append({
            'IdInventario': item.idInventario,
            'Codigo': item.codigoBarras,
            'Nombre': item.nombre,
            'Descripcion': item.descripcion,
            'Existencias': item.cantidadActual,
            'CantidadMinima': item.cantidadMinima,
            'PrecioCompra': item.precioCompra,
            'PrecioMayoreo': item.mayoreo,
            'PrecioMenudeo': item.menudeo,
            'PrecioColocado': item.colocado,
            'TipoMedida': item.tipoMedida,
            'Proveedor': item.proveedorEmpresa,
            'Categoria': item.categoriaNombre,
            'Aplicaciones': aplicaciones
        })

    return productos


# OBTENER INFORMACION DE PRODUCTOS ACTIVOS PERO BAJOS EN STOCK
def obtener_stock_bajo():
    # Realizar la consulta para obtener los productos activos y bajos en stock
    query = db.session.query(
        Inventario.idInventario,
        Inventario.codigoBarras,
        Inventario.nombre,
        Inventario.descripcion,
        Inventario.cantidadActual,
        Inventario.cantidadMinima
    ).filter(
        Inventario.estado == 1,  # Productos activos
        or_(
            Inventario.cantidadMinima > Inventario.cantidadActual,  # Stock bajo
            Inventario.cantidadMinima == Inventario.cantidadActual  # Stock igual al mínimo
        )
    ).limit(100).all()

    producto_bajo = []

    # Iterar sobre los resultados de la consulta
    for item in query:
        producto_bajo.append({
            'IdInventario': item.idInventario,
            'Codigo': item.codigoBarras,
            'Nombre': item.nombre,
            'Descripcion': item.descripcion,
            'Existencias': item.cantidadActual,
            'CantidadMinima': item.cantidadMinima
        })

    return producto_bajo

# OBTENER INFO DE LOS PRODUCTOS DESACTIVADOS O PREVIAMENTE ELIMINADOS PERO DESACTIVADOS
def get_productos_eliminados(codigo_barras):
    query = db.session.query(
        Inventario.idInventario,
        Inventario.codigoBarras,
        Inventario.nombre,
        Inventario.descripcion,
        Inventario.cantidadActual,
        func.coalesce(Proveedor.empresa, 'SIN PROVEEDOR').label('proveedorEmpresa')
    ).outerjoin(
        ProveedorProducto, Inventario.idInventario == ProveedorProducto.idInventario
    ).outerjoin(
        Proveedor, ProveedorProducto.idProveedor == Proveedor.idProveedor
    ).filter(
        Inventario.estado == 0
    )
    if codigo_barras:
        query = query.filter(Inventario.codigoBarras.like(f"%{codigo_barras}%"))
        
    query = query.limit(100).all()

    producto_eliminado = []

    # Iterar sobre los resultados de la consulta
    for item in query:
        producto_eliminado.append({
            'IdInventario': item.idInventario,
            'Codigo': item.codigoBarras,
            'Nombre': item.nombre,
            'Descripcion': item.descripcion,
            'Existencias': item.cantidadActual,
            'Proveedor': item.proveedorEmpresa
        })

    return producto_eliminado


# CREAR UN NUEVO PRODUCTO MEDIANTE VARIOS PROCEDIMIENTOS ALMACENADOS
def crear_producto(codigoBarras, nombre, descripcion, cantidadActual, cantidadMinima, precioCompra, mayoreo, 
                   menudeo, colocado, idUnidadMedida, idCategoria, idProveedor, idUsuario, imagenes, vehiculos):
    session = db.session

    try:
        with session.begin():  # Iniciar la transacción

            # Paso 1: Verificar si el producto ya existe
            producto_existente = session.execute(
                text("SELECT COUNT(*) FROM inventario WHERE codigoBarras = :codigoBarras"),
                {'codigoBarras': codigoBarras}
            ).scalar()

            if producto_existente > 0:
                # Si el producto ya existe, devolver un error con código 409
                return {"error": f"El producto con este código '{codigoBarras}' ya existe.", "code": 409}

            # Procedimiento 1: Insertar producto y obtener idInventario
            sql = text("""
                CALL proc_insertar_producto(:idCategoria, :idUnidadMedida, :codigoBarras, :nombre, :descripcion, 
                :cantidadActual, :cantidadMinima, :precioCompra, :mayoreo, :menudeo, :colocado, 
                :idProveedor, :idUsuario, @p_idInventario)
            """)
            session.execute(sql, {
                'idCategoria': idCategoria,
                'idUnidadMedida': idUnidadMedida,
                'codigoBarras': codigoBarras,
                'nombre': nombre,
                'descripcion': descripcion,
                'cantidadActual': cantidadActual,
                'cantidadMinima': cantidadMinima,
                'precioCompra': precioCompra,
                'mayoreo': mayoreo,
                'menudeo': menudeo,
                'colocado': colocado,
                'idProveedor': idProveedor,
                'idUsuario': idUsuario
            })

            # Obtener el ID del producto insertado
            result = session.execute(text("SELECT @p_idInventario")).first()
            id_inventario = result[0]

            # Procedimiento 2: Insertar imágenes para el producto
            sql = text("""
                CALL proc_inserta_img_producto(:idInventario, :imagenes)
            """)
            session.execute(sql, {
                'idInventario': id_inventario,
                'imagenes': imagenes
            })

            # Procedimiento 3: Procesar cada vehículo, recolectar los IDs generados
            modelo_anios_ids = []
            for vehiculo in vehiculos:
                sql = text("""
                    CALL proc_insertar_modelos(:idModelo, :anioInicio, :anioFin, :anioTodo, @p_idModeloAnio)
                """)
                session.execute(sql, {
                    'idModelo': vehiculo['idModelo'],
                    'anioInicio': vehiculo['anioInicio'],
                    'anioFin': vehiculo['anioFin'],
                    'anioTodo': vehiculo['todoAnio']
                })

                # Obtener el ID del modelo-año generado
                result = session.execute(text("SELECT @p_idModeloAnio")).first()
                modelo_anio_id = result[0]
                
                if modelo_anio_id:
                    modelo_anios_ids.append(modelo_anio_id)

            # Convertir la lista de IDs a una cadena separada por comas
            modelo_anios_ids_str = ','.join(map(str, modelo_anios_ids))

            # Procedimiento 4: Relacionar el producto con los IDs de los modelos-años
            sql = text("""
                CALL proc_relate_producto_modeloanios(:idInventario, :modelosAnios)
            """)
            session.execute(sql, {
                'idInventario': id_inventario,
                'modelosAnios': modelo_anios_ids_str
            })

        # Si llegamos aquí, todo salió bien, y se hace commit automáticamente
        return id_inventario

    except Exception as e:
        # Manejo de errores, hacer rollback
        session.rollback()
        return {"error": str(e)}

# FUNCION PARA EDITAR UN PRODUCTO ACTIVO
def modificar_producto(idInventario, codigoBarras, nombre, descripcion, cantidadActual, cantidadMinima, precioCompra, mayoreo, 
                   menudeo, colocado, idUnidadMedida, idCategoria, idProveedor, imagenes, vehiculos):
    session = db.session
    imagenes_list = imagenes.split(',')
    try:
        with session.begin():  # Iniciar la transacción
            # Procedimiento 1: Modificar un producto mediante su ID
            sql = text("""
                CALL proc_actualizar_producto_con_comparacion(:idInventario, :idCategoria, :idUnidadMedida, :codigoBarras, 
                :nombre, :descripcion, :cantidadActual, :cantidadMinima, :precioCompra, :mayoreo, :menudeo, :colocado, 
                :idProveedor)
            """)
            session.execute(sql, {
                'idInventario':idInventario,
                'idCategoria': idCategoria,
                'idUnidadMedida': idUnidadMedida,
                'codigoBarras': codigoBarras,
                'nombre': nombre,
                'descripcion': descripcion,
                'cantidadActual': cantidadActual,
                'cantidadMinima': cantidadMinima,
                'precioCompra': precioCompra,
                'mayoreo': mayoreo,
                'menudeo': menudeo,
                'colocado': colocado,
                'idProveedor': idProveedor
            })

            # Procedimiento 2: Modificar imágenes para el producto
            for i, imagen in enumerate(imagenes_list):
                if imagen.lower() == 'false':
                    image_path = os.path.join(IMAGE_ROOT_PATH,f"{codigoBarras}_{i+1}.webp")
                    if os.path.exists(image_path):
                        os.remove(image_path)

            sql = text("""
                CALL proc_actualiza_img_producto(:idInventario, :imagenes)
            """)
            session.execute(sql, {
                'idInventario': idInventario,
                'imagenes': imagenes
            })

            # Procedimiento 3: Procesar cada vehículo, recolectar los IDs generados en Editar
            modelo_anios_ids = []
            for vehiculo in vehiculos:
                sql = text("""
                    CALL proc_insertar_modelos(:idModelo, :anioInicio, :anioFin, :anioTodo, @p_idModeloAnio)
                """)
                session.execute(sql, {
                    'idModelo': vehiculo['idModelo'],
                    'anioInicio': vehiculo['anioInicio'],
                    'anioFin': vehiculo['anioFin'],
                    'anioTodo': vehiculo['todoAnio']
                })

                # Obtener el ID del modelo-año generado
                result = session.execute(text("SELECT @p_idModeloAnio")).first()
                modelo_anio_id = result[0]
                
                if modelo_anio_id:
                    modelo_anios_ids.append(modelo_anio_id)

            # Convertir la lista de IDs a una cadena separada por comas
            modelo_anios_ids_str = ','.join(map(str, modelo_anios_ids))

            # Procedimiento 4: Relacionar el producto con los IDs de los modelos-años
            sql = text("""
                CALL proc_editar_producto_modeloanios(:idInventario, :nuevaListaModelosAnios)
            """)
            session.execute(sql, {
                'idInventario': idInventario,
                'nuevaListaModelosAnios': modelo_anios_ids_str
            })

        # Si llegamos aquí, todo salió bien, y se hace commit automáticamente
        return idInventario

    except DBAPIError as e:
        session.rollback()
        error_message = e.orig.args[1]  # Obtener el mensaje de error
        raise ValueError(f'Ocurrió un error: {error_message}')
    except SQLAlchemyError as e:
        # Manejo de errores, hacer rollback
        session.rollback()
        raise ValueError(f'Ocurrió un error: {str(e)}')
    except Exception as e:
        session.rollback() 
        raise ValueError(f'Ocurrió un error: {str(e)}')



# FUNCIÓN PARA ELIMINAR UN PRODUCTO ACTIVO Y SUS IMÁGENES
def eliminar_producto(idInventario, idUsuario):
    session = db.session  # Obtener la sesión de la base de datos

    try:
        # Verificar si el producto existe y está activo
        producto = session.query(Inventario).filter_by(idInventario=idInventario, estado=True).first()
        if producto is None:
            return "no_existe"  # Indica que el producto no existe o no está activo

        # Iniciar la transacción solo si no hay una activa
        if not session.is_active:
            session.begin()

        # Paso 1: Eliminar las imágenes del servidor
        eliminar_imagenes_del_servidor(idInventario)

        # Paso 2: Actualizar las imágenes en la base de datos (marcar como 'false')
        sql_update_img = text("CALL proc_actualiza_img_producto(:idInventario, :imagenes)")
        session.execute(sql_update_img, {'idInventario': idInventario, 'imagenes': 'false,false,false,false,false'})

        # Paso 3: Llamar al procedimiento almacenado para eliminar el producto
        sql = text("CALL proc_eliminar_producto(:idInventario, :idUsuario)")
        session.execute(sql, {'idInventario': idInventario, 'idUsuario': idUsuario})

        session.commit()  # Confirmar los cambios

        return {'message': 'Producto y sus imágenes eliminados correctamente'}

    except SQLAlchemyError as e:
        session.rollback()  # Hacer rollback en caso de error
        return {"error": str(e)}

# FUNCIÓN PARA ELIMINAR LAS IMÁGENES DEL SERVIDOR
def eliminar_imagenes_del_servidor(idInventario):
    try:
        # Obtener el código de barras y las imágenes relacionadas usando el idInventario
        query = db.session.query(
            Inventario.codigoBarras,
            Imagenes.imgRepresentativa,
            Imagenes.img2,
            Imagenes.img3,
            Imagenes.img4,
            Imagenes.img5
        ).outerjoin(
            Imagenes, Imagenes.idInventario == idInventario
        ).filter(
            Inventario.idInventario == idInventario
        ).first()

        if query is None:
            return  # Simplemente salimos sin hacer nada

        codigo_barras = query.codigoBarras

        # Paso 1: Eliminar las imágenes correspondientes al código de barras
        for imagenId, imagen_field in enumerate(
            [query.imgRepresentativa, query.img2, query.img3, query.img4, query.img5], start=1
        ):
            if imagen_field:  # Si la imagen está presente
                image_path = os.path.join(IMAGE_ROOT_PATH,f"{codigo_barras}_{imagenId}.webp")
                
                # Verificar si el archivo existe y eliminarlo
                if os.path.exists(image_path):
                    os.remove(image_path)
                else:
                    print(f"La imagen no existe o ya fue eliminada: {image_path}")
            else:
                print(f"No hay imagen en el campo {imagenId} para el código de barras {codigo_barras}.")

    except Exception as e:
        print(f"Error al eliminar imágenes: {str(e)}")


# FUNCION PARA REACTIVAR UN PRODUCTO QUE FUE ELIMINADO Y SU ESTADO ESTA EN FALSE
def reactivar_producto(idInventario):
    session = db.session  # Obtener la sesión de base de datos

    try:
        with session.begin():  # Iniciar la transacción
        # Verificar si el producto existe y está en estado False
            producto = session.query(Inventario).filter_by(idInventario=idInventario, estado=False).first()
            if producto is None:
                return "no_valido"  # Si el producto no existe o no está inactivo, retornamos "no_valido"

            # Llamar al procedimiento almacenado usando text para pasar el parámetro de manera segura
            sql = text("CALL proc_reactivar_producto(:idInventario)")
            session.execute(sql, {'idInventario': idInventario})

        # Si llegamos aquí, la transacción se completa con éxito (commit automático con `with session.begin()`)
        return {'message': 'Producto reactivado correctamente'}

    except SQLAlchemyError as e:
        # Manejo de errores, hacer rollback
        session.rollback()
        return {"error": str(e)}

### FUNCION PARA AGREGAR EXISTENCIAS A UN PRODUCTO
def agregar_existencias_producto(idUsuario, idInventario, cantidadNueva, precioCompra, mayoreo, menudeo, colocado):
    session = db.session  # Obtener la sesión de la base de datos

    try:

        # Si ambos existen, continuar con la operación
        with session.begin():  # Iniciar una transacción

            # Verificar si el usuario existe
            usuario_existe = session.execute(text("SELECT COUNT(*) FROM Usuarios WHERE idUsuario = :idUsuario"), {'idUsuario': idUsuario}).scalar()

            if usuario_existe == 0:
                return {'error': 'El idUsuario no existe en el sistema.'}

            # Verificar si el inventario existe
            inventario_existe = session.execute(text("SELECT COUNT(*) FROM Inventario WHERE idInventario = :idInventario"), {'idInventario': idInventario}).scalar()

            if inventario_existe == 0:
                return {'error': 'El idInventario no existe en el sistema.'}
            
            # Llamar al procedimiento almacenado usando `text` para prevenir inyección SQL
            sql = text("CALL proc_insertar_entrada_producto(:idUsuario, :idInventario, :cantidadNueva, :precioCompra, :mayoreo, :menudeo, :colocado)")
            session.execute(sql, {
                'idUsuario': idUsuario,
                'idInventario': idInventario,
                'cantidadNueva': cantidadNueva,
                'precioCompra': precioCompra,
                'mayoreo': mayoreo,
                'menudeo': menudeo,
                'colocado': colocado
            })

        # Si se llega aquí, la transacción se completa con éxito (commit automático con `with session.begin()`)
        return {'message': 'Existencias agregadas al producto correctamente'}

    except Exception as e:
        session.rollback()  # Revertir la transacción en caso de error
        return {'error': f'Ocurrió un error: {str(e)}'}


### FUNCION PARA LA FUNCION DE IMPORTAR PRODUCTOS
def obtener_id_inventario(codigo):
    resultado = db.session.query(
        Inventario.idInventario
    ).filter(
        Inventario.codigoBarras == codigo
    ).first()
    return resultado[0] if resultado else None

def obtener_imagen(idInventario, imagenId):
    query = db.session.query(
        Inventario.codigoBarras,
        Imagenes.imgRepresentativa,
        Imagenes.img2,
        Imagenes.img3,
        Imagenes.img4,
        Imagenes.img5
    ).outerjoin(
        Inventario, Imagenes.idInventario == Inventario.idInventario
    ).filter(
        Imagenes.idInventario == idInventario
    ).first()

    if query is None:
        raise ValueError("Producto no encontrado")

    image_path = None
    if imagenId == 1 and query.imgRepresentativa:
        image_path = os.path.join(IMAGE_ROOT_PATH,f"{query.codigoBarras}_1.webp")
    elif imagenId == 2 and query.img2:
        image_path = os.path.join(IMAGE_ROOT_PATH,f"{query.codigoBarras}_2.webp")
    elif imagenId == 3 and query.img3:
        image_path = os.path.join(IMAGE_ROOT_PATH,f"{query.codigoBarras}_3.webp")
    elif imagenId == 4 and query.img4:
        image_path = os.path.join(IMAGE_ROOT_PATH,f"{query.codigoBarras}_4.webp")
    elif imagenId == 5 and query.img5:
        image_path = os.path.join(IMAGE_ROOT_PATH,f"{query.codigoBarras}_5.webp")

    if image_path is None:
        raise ValueError("Imagen no encontrada")

    return image_path