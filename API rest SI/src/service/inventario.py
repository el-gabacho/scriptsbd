from sqlalchemy import func, case
from sqlalchemy.exc import DBAPIError
from models import db, Inventario, ProveedorProducto, ModeloAutoparte, ModeloAnio, Modelo, Marca, Anio, UnidadMedida, Imagenes
from categorias.Domain.Categoria import Categoria
from proveedores.Domain.Proveedor import Proveedor

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
        Proveedor.empresa.label('proveedorEmpresa'),
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
    ).join(
        ProveedorProducto, Inventario.idInventario == ProveedorProducto.idInventario
    ).join(
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
    ).all()

    productos_list = []
    for producto in query:
        aplicaciones = producto.aplicaciones
        if not aplicaciones:
            aplicaciones = ["SIN NINGUNA APLICACION"]
        else:
            aplicaciones = [app.strip() for app in aplicaciones.split(',') if app.strip()]

        # Construir la lista de imágenes
        base_path = "C:\\imagenes_el_gabacho\\productosInventario"
        imagenes = []
        if producto.imgRepresentativa:
            imagenes.append(f"{base_path}\\{producto.codigoBarras}_1.png")
        if producto.img2:
            imagenes.append(f"{base_path}\\{producto.codigoBarras}_2.png")
        if producto.img3:
            imagenes.append(f"{base_path}\\{producto.codigoBarras}_3.png")
        if producto.img4:
            imagenes.append(f"{base_path}\\{producto.codigoBarras}_4.png")
        if producto.img5:
            imagenes.append(f"{base_path}\\{producto.codigoBarras}_5.png")

        if not imagenes:
            imagenes.append('SIN IMAGEN')

        productos_list.append({
            'idInventario': producto.idInventario,
            'codigo': producto.codigoBarras,
            'nombre': producto.nombre,
            'descripcion': producto.descripcion,
            'existencias': producto.cantidadActual,
            'cantidadMinima': producto.cantidadMinima,
            'precioCompra': producto.precioCompra,
            'precioMayoreo': producto.mayoreo,
            'precioMenudeo': producto.menudeo,
            'precioColocado': producto.colocado,
            'tipoMedida': producto.tipoMedida,
            'proveedor': producto.proveedorEmpresa,
            'categoria': producto.categoriaNombre,
            'aplicaciones': aplicaciones,
            'imagenes': imagenes
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
        Inventario.cantidadMinima,
        Inventario.precioCompra,
        Inventario.mayoreo,
        Inventario.menudeo,
        Inventario.colocado,
        Inventario.estado,
        UnidadMedida.tipoMedida,
        func.coalesce(Categoria.nombre, 'SIN CATEGORIA').label('categoriaNombre'),
        Proveedor.empresa.label('proveedorEmpresa'),
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
    ).join(
        ProveedorProducto, Inventario.idInventario == ProveedorProducto.idInventario
    ).join(
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
    ).group_by(
        Inventario.idInventario
    ).first()

    if query is None:
        return {'error': 'Producto no encontrado'}

    # Procesar el campo de aplicaciones
    aplicaciones = query.aplicaciones
    if aplicaciones:
        aplicaciones = [app.strip() for app in aplicaciones.split(',') if app.strip()]
    else:
        aplicaciones = ["SIN NINGUNA APLICACION"]

    # Construir la lista de imágenes
    base_path = "C:\\imagenes_el_gabacho\\productosInventario"
    imagenes = []
    if query.imgRepresentativa:
        imagenes.append(f"{base_path}\\{query.codigoBarras}_1.png")
    if query.img2:
        imagenes.append(f"{base_path}\\{query.codigoBarras}_2.png")
    if query.img3:
        imagenes.append(f"{base_path}\\{query.codigoBarras}_3.png")
    if query.img4:
        imagenes.append(f"{base_path}\\{query.codigoBarras}_4.png")
    if query.img5:
        imagenes.append(f"{base_path}\\{query.codigoBarras}_5.png")

    if not imagenes:
        imagenes.append('SIN IMAGEN')

    producto = {
        'idInventario': query.idInventario,
        'codigo': query.codigoBarras,
        'NombreProducto': query.nombre,
        'descripcion': query.descripcion,
        'Existencias': query.cantidadActual,
        'cantidadMinima': query.cantidadMinima,
        'precioCompra': query.precioCompra,
        'precioMayoreo': query.mayoreo,
        'precioMenudeo': query.menudeo,
        'precioColocado': query.colocado,
        'tipoMedida': query.tipoMedida,
        'proveedor': query.proveedorEmpresa,
        'categoria': query.categoriaNombre,
        'Aplicaciones': aplicaciones,
        'imagenes': imagenes
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
        Proveedor.empresa.label('proveedorEmpresa'),
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
    ).join(
        ProveedorProducto, Inventario.idInventario == ProveedorProducto.idInventario
    ).join(
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
    ).all()


    productos = []
    base_path = "C:\\imagenes_el_gabacho\\productosInventario"
    for item in query:
        aplicaciones = item.aplicaciones
        if aplicaciones:
            aplicaciones = [app.strip() for app in aplicaciones.split(',') if app.strip()]
        else:
            aplicaciones = ["SIN NINGUNA APLICACION"]

        imagenes = []
        if item.imgRepresentativa:
            imagenes.append(f"{base_path}\\{item.codigoBarras}_1.png")
        if item.img2:
            imagenes.append(f"{base_path}\\{item.codigoBarras}_2.png")
        if item.img3:
            imagenes.append(f"{base_path}\\{item.codigoBarras}_3.png")
        if item.img4:
            imagenes.append(f"{base_path}\\{item.codigoBarras}_4.png")
        if item.img5:
            imagenes.append(f"{base_path}\\{item.codigoBarras}_5.png")

        if not imagenes:
            imagenes.append('SIN IMAGEN')

        productos.append({
            'idInventario': item.idInventario,
            'codigo': item.codigoBarras,
            'nombre': item.nombre,
            'descripcion': item.descripcion,
            'existencias': item.cantidadActual,
            'cantidadMinima': item.cantidadMinima,
            'precioCompra': item.precioCompra,
            'precioMayoreo': item.mayoreo,
            'precioMenudeo': item.menudeo,
            'precioColocado': item.colocado,
            'tipoMedida': item.tipoMedida,
            'proveedor': item.proveedorEmpresa,
            'categoria': item.categoriaNombre,
            'aplicaciones': aplicaciones,
            'imagenes': imagenes
        })

    return productos

# XDDDDDDDDDDDDDDDDDDDDDDDD
def buscar_inventarios(filtros):
    query = db.session.query(
        Inventario.idInventario,
        Inventario.codigoBarras,
        Inventario.nombre,
        Inventario.descripcion,
        Inventario.cantidadActual,
        Proveedor.empresa,
        Marca.nombre.label('marca'),
        Modelo.nombre.label('modelo'),
        func.concat(func.coalesce(Anio.anioInicio, ''), '-', func.coalesce(Anio.anioFin, '')).label('anioRango')
    ).join(
        Categoria, Inventario.idCategoria == Categoria.idCategoria
    ).join(
        ProveedorProducto, Inventario.idInventario == ProveedorProducto.idInventario
    ).join(
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
    )

    if filtros.get('codigoBarras'):
        query = query.filter(Inventario.codigoBarras.like(f"%{filtros['codigoBarras']}%"))
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
    if filtros.get('anio'):
        query = query.filter(func.concat(func.coalesce(Anio.anioInicio, ''), '-', func.coalesce(Anio.anioFin, '')) == filtros['anio'])

    resultados = query.all()

    inventarios = []
    for resultado in resultados:
        inventarios.append({
            'idInventario': resultado.idInventario,
            'codigoBarras': resultado.codigoBarras,
            'nombre': resultado.nombre,
            'descripcion': resultado.descripcion,
            'cantidadActual': resultado.cantidadActual,
            'empresa': resultado.empresa,
            'marca': resultado.marca,
            'modelo': resultado.modelo,
            'anioRango': resultado.anioRango,
        })

    return inventarios

def obtener_stock_bajo():
    stock_bajo = Inventario.query.filter(Inventario.cantidadMinima > Inventario.cantidadActual).all()
    return stock_bajo

def crear_producto(codigoBarras, nombre, descripcion, cantidadActual, cantidadMinima, precioCompra, mayoreo, 
                   menudeo, colocado, idUnidadMedida, idCategoria, idProveedor, idUsuario, id_modeloAnio):
    try:
        # Llamar al procedimiento almacenado para insertar un producto en el inventario
        db.session.execute(
        f"CALL proc_insertar_producto({idCategoria}, {idUnidadMedida}, {codigoBarras}, {nombre}, {descripcion}, {cantidadActual}, {cantidadMinima}, {precioCompra}, {mayoreo}, {menudeo}, {colocado}, {idProveedor}, {idUsuario}, @v_idInventario)"
        )
        result = db.session.execute("SELECT @v_idInventario").first()
        id_inventario = result[0]

        # Llamar al procedimiento almacenado para relacionar un modeloanio con un Autoparte del Inventario
        db.session.execute(f"CALL proc_modeloanio_autoparte({id_inventario}, {id_modeloAnio})")

        # Confirmar los cambios en la base de datos
        db.session.commit()

        # Cerrar la sesión
        db.session.close()
        return id_inventario
    except DBAPIError as e:
        return str(e)

def eliminar_producto(idInventario, idUsuario):
    # Llamar al procedimiento almacenado para eliminar un producto del inventario
    db.session.execute(f"CALL proc_eliminar_producto({idInventario},{idUsuario})")

    # Confirmar los cambios en la base de datos
    db.session.commit()

    # Cerrar la sesión
    db.session.close()