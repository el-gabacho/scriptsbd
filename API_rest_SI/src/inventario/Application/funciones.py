from proveedores.Domain.Proveedor import Proveedor
from sqlalchemy import func, case, or_
from sqlalchemy.exc import DBAPIError, SQLAlchemyError
from init import db
from inventario.Domain.Inventario import Inventario, UnidadMedida, Imagenes
from categorias.Domain.Categoria import Categoria
from proveedores.Domain.Proveedor import Proveedor
from proveedores.Domain.ProveedorProducto import ProveedorProducto
from vehiculos.Domain.ModeloAutoparte import ModeloAutoparte
from vehiculos.Domain.ModeloAnio import ModeloAnio
from vehiculos.Domain.Modelo import Modelo
from vehiculos.Domain.Marca import Marca
from vehiculos.Domain.Anio import Anio

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
            imagenes.append(f"{base_path}\\{producto.codigoBarras}_1.webp")
        if producto.img2:
            imagenes.append(f"{base_path}\\{producto.codigoBarras}_2.webp")
        if producto.img3:
            imagenes.append(f"{base_path}\\{producto.codigoBarras}_3.webp")
        if producto.img4:
            imagenes.append(f"{base_path}\\{producto.codigoBarras}_4.webp")
        if producto.img5:
            imagenes.append(f"{base_path}\\{producto.codigoBarras}_5.webp")

        if not imagenes:
            imagenes.append('SIN IMAGEN')

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
            'Imagenes': imagenes
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
        imagenes.append(f"{base_path}\\{query.codigoBarras}_1.webp")
    if query.img2:
        imagenes.append(f"{base_path}\\{query.codigoBarras}_2.webp")
    if query.img3:
        imagenes.append(f"{base_path}\\{query.codigoBarras}_3.webp")
    if query.img4:
        imagenes.append(f"{base_path}\\{query.codigoBarras}_4.webp")
    if query.img5:
        imagenes.append(f"{base_path}\\{query.codigoBarras}_5.webp")

    if not imagenes:
        imagenes.append('SIN IMAGEN')

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
        'Imagenes': imagenes
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
            imagenes.append(f"{base_path}\\{item.codigoBarras}_1.webp")
        if item.img2:
            imagenes.append(f"{base_path}\\{item.codigoBarras}_2.webp")
        if item.img3:
            imagenes.append(f"{base_path}\\{item.codigoBarras}_3.webp")
        if item.img4:
            imagenes.append(f"{base_path}\\{item.codigoBarras}_4.webp")
        if item.img5:
            imagenes.append(f"{base_path}\\{item.codigoBarras}_5.webp")

        if not imagenes:
            imagenes.append('SIN IMAGEN')

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
            'Imagenes': imagenes
        })

    return productos

# OBTENER INFORMACION DE PRODUCTOS ACTIVOS MEDIANTE DICHA INFORMACION DE MODO SIMILITUD
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
            'IdInventario': resultado.idInventario,
            'CodigoBarras': resultado.codigoBarras,
            'Nombre': resultado.nombre,
            'Descripcion': resultado.descripcion,
            'CantidadActual': resultado.cantidadActual,
            'Empresa': resultado.empresa,
            'Marca': resultado.marca,
            'Modelo': resultado.modelo,
            'AnioRango': resultado.anioRango,
        })

    return inventarios

def obtener_stock_bajo():
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
        or_(
            Inventario.cantidadMinima > Inventario.cantidadActual,
            Inventario.cantidadMinima == Inventario.cantidadActual
        )
    ).group_by(
        Inventario.idInventario
    ).all()

    producto_bajo = []
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

        producto_bajo.append({
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
            'Imagenes': imagenes
        })

    return producto_bajo

def crear_producto(codigoBarras, nombre, descripcion, cantidadActual, cantidadMinima, precioCompra, mayoreo, 
                   menudeo, colocado, idUnidadMedida, idCategoria, idProveedor, idUsuario, imagenes, vehiculos):
    session = db.session
    try:
        with session.begin():  # Iniciar la transacción
            # Procedimiento 1: Insertar producto y obtener idInventario
            session.execute(
                "CALL proc_insertar_producto(:idCategoria, :idUnidadMedida, :codigoBarras, :nombre, :descripcion, "
                ":cantidadActual, :cantidadMinima, :precioCompra, :mayoreo, :menudeo, :colocado, "
                ":idProveedor, :idUsuario, @p_idInventario)",
                {
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
                }
            )

            # Obtener el ID del producto insertado
            result = session.execute("SELECT @p_idInventario").first()
            id_inventario = result[0]
            
            if not id_inventario:
                raise Exception("No se obtuvo el ID del inventario después de insertar el producto.")
            
            # Procedimiento 2: Insertar imágenes para el producto
            session.execute(
                "CALL proc_inserta_img_producto(:idInventario, :imagenes)",
                {
                    'idInventario': id_inventario,
                    'imagenes': imagenes  # Pasar la cadena de imágenes como string
                }
            )

            # Procedimiento 3: Procesar cada vehículo, recolectar los IDs generados
            modelo_anios_ids = []
            for vehiculo in vehiculos:
                session.execute(
                    "CALL proc_insertar_modelos(:idModelo, :anioInicio, :anioFin, :anioTodo, @p_idModeloAnio)",
                    {
                        'idModelo': vehiculo['idModelo'],
                        'anioInicio': vehiculo['añoInicio'],
                        'anioFin': vehiculo['añoFin'],
                        'anioTodo': vehiculo['todoAño']
                    }
                )
                
                # Obtener el ID del modelo-año generado
                result = session.execute("SELECT @p_idModeloAnio").first()
                modelo_anio_id = result[0]
                
                if modelo_anio_id:
                    modelo_anios_ids.append(modelo_anio_id)

            # Convertir la lista de IDs a una cadena separada por comas
            modelo_anios_ids_str = ','.join(map(str, modelo_anios_ids))

            # Procedimiento 4: Relacionar el producto con los IDs de los modelos-años
            session.execute(
                "CALL proc_relate_producto_modeloanios(:idInventario, :modelosAnios)",
                {
                    'idInventario': id_inventario,
                    'modelosAnios': modelo_anios_ids_str
                }
            )

        # Si llegamos aquí, todo salió bien, y se hace commit automáticamente
        return id_inventario

    except SQLAlchemyError as e:
        # Manejo de errores, hacer rollback
        session.rollback()
        return {"error": str(e)}
    except Exception as e:
        # Captura de otros errores
        session.rollback()
        return {"error": str(e)}


def eliminar_producto(idInventario, idUsuario):
    # Llamar al procedimiento almacenado para eliminar un producto del inventario
    db.session.execute(f"CALL proc_eliminar_producto({idInventario},{idUsuario})")

    # Confirmar los cambios en la base de datos
    db.session.commit()

    # Cerrar la sesión
    db.session.close()