from sqlalchemy import func
from sqlalchemy.exc import DBAPIError
from models import db, Inventario, Proveedor, ProveedorProducto, Categoria, ModeloAutoparte, ModeloAnio, Modelo, Marca, Anio, UnidadMedida

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
        UnidadMedida.tipoMedida,
        Categoria.nombre.label('categoriaNombre'),
        Proveedor.empresa.label('proveedorEmpresa'),
        func.group_concat(
            func.concat(
                Marca.nombre, ' ', Modelo.nombre, ' ', 
                func.coalesce(Anio.anioInicio, ''), '-', 
                func.coalesce(Anio.anioFin, '')
            ).distinct()
        ).label('Aplicaciones')
    ).join(
        UnidadMedida, Inventario.idUnidadMedida == UnidadMedida.idUnidadMedida
    ).join(
        ProveedorProducto, Inventario.idInventario == ProveedorProducto.idInventario
    ).join(
        Proveedor, ProveedorProducto.idProveedor == Proveedor.idProveedor
    ).join(
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
    ).group_by(
        Inventario.idInventario
    ).all()

    productos_list = []
    for producto in query:
        productos_list.append({
            'idInventario': producto.idInventario,
            'codigo': producto.codigoBarras,
            'NombreProducto': producto.nombre,
            'descripcion': producto.descripcion,
            'Existencias': producto.cantidadActual,
            'cantidadMinima': producto.cantidadMinima,
            'precioCompra': producto.precioCompra,
            'precioMayoreo': producto.mayoreo,
            'precioMenudeo': producto.menudeo,
            'precioColocado': producto.colocado,
            'tipoMedida': producto.tipoMedida,
            'proveedor': producto.proveedorEmpresa,
            'categoria': producto.categoriaNombre,
            'Aplicaciones': producto.Aplicaciones.split(',')
        })

    return productos_list

def get_producto(codigo_barras):
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
        UnidadMedida.tipoMedida,
        Categoria.nombre.label('categoriaNombre'),
        Proveedor.empresa.label('proveedorEmpresa'),
        func.group_concat(
            func.concat(
                Marca.nombre, ' ', Modelo.nombre, ' ', 
                func.coalesce(Anio.anioInicio, ''), '-', 
                func.coalesce(Anio.anioFin, '')
            ).distinct()
        ).label('Aplicaciones')
    ).join(
        UnidadMedida, Inventario.idUnidadMedida == UnidadMedida.idUnidadMedida
    ).join(
        ProveedorProducto, Inventario.idInventario == ProveedorProducto.idInventario
    ).join(
        Proveedor, ProveedorProducto.idProveedor == Proveedor.idProveedor
    ).join(
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
    ).filter(Inventario.codigoBarras == codigo_barras).group_by(
        Inventario.idInventario
    ).first()

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
        'Aplicaciones': query.Aplicaciones.split(',')
    }
    return producto

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