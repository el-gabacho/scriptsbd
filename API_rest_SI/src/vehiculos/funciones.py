from init import db
from vehiculos.modelos import Marca, MarcaSchema, Modelo, ModeloAnio, Anio, ModeloAutoparte
from inventario.modelos import Inventario
from sqlalchemy import func, distinct
from sqlalchemy.exc import IntegrityError

marca_schema = MarcaSchema()
marcas_schema = MarcaSchema(many=True) 

# -----------------------------------------------------------------------------------------------------------------------------------

# CONSULTA PRINCIPAL DE VEHICULOS : MARCAS
# OBTIENE MARCAS CON SU NUMERO DE MODELOS

def get_marcas_count_modelos():
    marcas = db.session.query(
        Marca.idMarca,
        Marca.nombre,
        Marca.urlLogo,
        db.func.count(Modelo.idModelo).label('numeroModelos')
    ).outerjoin(
        Modelo, Marca.idMarca == Modelo.idMarca
    ).group_by(
        Marca.idMarca
    ).all()

    marcas_list = []
    for marca in marcas:
        marcas_list.append({
            'Id': marca.idMarca,
            'Nombre': marca.nombre,
            'UrlLogo': marca.urlLogo,
            'NumModelos': marca.numeroModelos
        })

    return marcas_list

# -----------------------------------------------------------------------------------------------------------------------------------

# CRUD DE MARCA: BUSCAR POR NOMBRE DE LA MARCA, REALIZAR UNA NUEVA MARCA, EDITAR MARCA Y ELIMINAR MARCA

def get_buscar_marcas_similar(nombremarca):
    marcas = db.session.query(
        Marca.idMarca,
        Marca.nombre,
        Marca.urlLogo,
        db.func.count(Modelo.idModelo).label('numeroModelos')
        ).outerjoin(
            Modelo, Marca.idMarca == Modelo.idMarca
        ).filter(
            Marca.nombre.like(f'%{nombremarca}%')
        ).group_by(
            Marca.idMarca
        ).all()
    
    marcas_list = []
    for marca in marcas:
        marcas_list.append({
            'Id': marca.idMarca,
            'Nombre': marca.nombre,
            'UrlLogo': marca.urlLogo,
            'NumModelos': marca.numeroModelos,
            })
        
        return marcas_list

# -----------------------------------------------------------------------------------------------------------------------------------

# CREAR UNA NUEVA MARCA
def crear_marca(nombre, urlLogo):
    # Verificar si la marca ya existe
    marca_existente = Marca.query.filter_by(nombre=nombre).first()
    if marca_existente:
        return 'marca_ya_existe'

    # Crear la nueva marca si no existe
    nueva_marca = Marca(nombre=nombre, urlLogo=urlLogo)
    db.session.add(nueva_marca)
    db.session.commit()

    return 'creacion_exitosa'

# -----------------------------------------------------------------------------------------------------------------------

# EDITAR UNA MARCA POR IDMARCA
def editar_marca(idMarca, nombre, urlLogo):
    # Buscar la marca por ID
    marca = Marca.query.get(idMarca)
    
    # Validar si la marca existe
    if not marca:
        return False

    # Verificar si el nombre ingresado es el mismo que ya tiene la marca
    if marca.nombre == nombre:
        # Si el nombre es el mismo, permitir que actualice solo el URL (si es necesario)
        if marca.urlLogo == urlLogo:
            return 'sin_cambio'  # No se hicieron cambios
        else:
            marca.urlLogo = urlLogo
            db.session.commit()
            return True

    # Verificar si ya existe otra marca con el mismo nombre
    marca_existente = Marca.query.filter(Marca.nombre.ilike(nombre)).first()
    
    # Si ya existe una marca con el nombre proporcionado y no es la que estamos editando
    if marca_existente and marca_existente.idMarca != idMarca:
        return 'ya_existe'

    # Actualizar el nombre y el URL
    marca.nombre = nombre
    marca.urlLogo = urlLogo

    # Guardar los cambios en la base de datos
    db.session.commit()
    return True

# -----------------------------------------------------------------------------------------------------------------------

# ELIMINAR UNA MARCA POR IDMARCA
def eliminar_marca(idMarca):
    # Buscar la marca por ID
    marca = Marca.query.get(idMarca)
    
    # Verificar si la marca existe
    if not marca:
        return 'marca_no_encontrada'
    
    # Verificar si la marca tiene referencias en la tabla modelos
    if Modelo.query.filter_by(idMarca=idMarca).first():
        return 'marca_tiene_referencias'
    
    # Eliminar la marca
    db.session.delete(marca)
    db.session.commit()
    
    return True

# -----------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------

# CONSULTA SECUNDARIA DE VEHICULOS : MARCAS (ID) : MODELOS
# OBTENER MODELOS CON NUMERO DE PRODUCTOS RELACIONADOS MEDIANTE ID DE LA MARCA
def get_modelos_count_productos(idMarca):
    resultados = db.session.query(
        Marca.idMarca,
        Modelo.idModelo,
        Modelo.nombre.label('nombreModelo'),
        func.count(distinct(Inventario.idInventario)).label('numeroProductos')
    ).join(
        Modelo, Marca.idMarca == Modelo.idMarca
    ).outerjoin(
        ModeloAnio, Modelo.idModelo == ModeloAnio.idModelo
    ).outerjoin(
        ModeloAutoparte, ModeloAnio.idModeloAnio == ModeloAutoparte.idModeloAnio
    ).outerjoin(
        Inventario, ModeloAutoparte.idInventario == Inventario.idInventario
    ).filter(
        Marca.idMarca == idMarca
    ).group_by(
        Modelo.idModelo
    ).all()

    modelos_list = []
    for resultado in resultados:
        modelos_list.append({
            'IdMarca': resultado.idMarca,
            'Id': resultado.idModelo,
            'Nombre': resultado.nombreModelo,
            'NumProductos': resultado.numeroProductos
            })

    return modelos_list
# -----------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------
# CRUD DE MODELOS: BUSCAR POR NOMBRE DEL MODELO, REALIZAR UN NUEVO MODELO, EDITAR MODELO Y ELIMINAR MODELO
def get_buscar_modelos_similar(idMarca,nombremodelo):
    resultados = db.session.query(
        Marca.idMarca,
        Modelo.idModelo,
        Modelo.nombre.label('nombreModelo'),
        func.count(distinct(Inventario.idInventario)).label('numeroProductos')
    ).join(
        Modelo, Marca.idMarca == Modelo.idMarca
    ).outerjoin(
        ModeloAnio, Modelo.idModelo == ModeloAnio.idModelo
    ).outerjoin(
        ModeloAutoparte, ModeloAnio.idModeloAnio == ModeloAutoparte.idModeloAnio
    ).outerjoin(
        Inventario, ModeloAutoparte.idInventario == Inventario.idInventario
    ).filter(
        Marca.idMarca == idMarca,
        Modelo.nombre.like(f'%{nombremodelo}%')
    ).group_by(
        Modelo.idModelo
    ).all()

    modelos_list = []
    for resultado in resultados:
        modelos_list.append({
            'IdMarca': resultado.idMarca,
            'Id': resultado.idModelo,
            'Nombre': resultado.nombreModelo,
            'NumProductos': resultado.numeroProductos
            })

    return modelos_list

# CREAR UN NUEVO MODELO
def crear_modelo(idMarca,nombre):
    nuevo_modelo = Modelo(idMarca = idMarca, nombre=nombre)
    db.session.add(nuevo_modelo)
    db.session.commit()
    return nuevo_modelo.idModelo

# EDITAR UNA MARCA POR IDMARCA
def editar_modelo(idModelo, nombre):
    modelo = Modelo.query.get(idModelo)
    modelo.nombre = nombre
    db.session.commit()
    return True

# ELIMINAR UNA MARCA POR IDMARCA
def eliminar_modelo(idModelo):
    modelo = Modelo.query.get(idModelo)
    db.session.delete(modelo)
    db.session.commit()
    return True

# -----------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------
# Para la funcion de importar productos 

def obtener_id_marca(marca):
    resultado = db.session.query(
        Marca.idMarca
    ).filter(
        Marca.nombre == marca
    ).first()
    return resultado[0] if resultado else None

def obtener_id_modelo(id_marca, modelo):
    resultado = db.session.query(
        Modelo.idModelo
    ).join(
        Marca, Modelo.idMarca == Marca.idMarca
    ).filter(
        Modelo.nombre == modelo, Modelo.idMarca == id_marca
    ).first()
    return resultado[0] if resultado else None

def obtener_id_anio(anio_inicio, anio_fin):
    resultado = db.session.query(
        Anio.idAnio
    ).filter(
        Anio.anioInicio == anio_inicio, Anio.anioFin == anio_fin
    ).first()
    return resultado[0] if resultado else None

def obtener_id_modelo_anio(id_modelo, id_anio):
    resultado = db.session.query(
        ModeloAnio.idModeloAnio
    ).filter(
        ModeloAnio.idModelo == id_modelo, ModeloAnio.idAnio == id_anio
    ).first()
    return resultado[0] if resultado else None