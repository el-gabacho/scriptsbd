from init import db
from vehiculos.modelos import Marca, MarcaSchema, Modelo, ModeloAnio, Anio, ModeloAutoparte
from inventario.modelos import Inventario
from sqlalchemy import func, distinct
from sqlalchemy.exc import IntegrityError

marca_schema = MarcaSchema()
marcas_schema = MarcaSchema(many=True) 

# -----------------------------------------------------------------------------------------------------------------------------------
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

# CREAR UNA NUEVA MARCA
def crear_marca(nombre, urlLogo):
    nueva_marca = Marca(nombre=nombre, urlLogo=urlLogo)
    db.session.add(nueva_marca)
    db.session.commit()
    return nueva_marca.idMarca

# EDITAR UNA MARCA POR IDMARCA
def editar_marca(idMarca, nombre, urlLogo):
    marca = Marca.query.get(idMarca)
    marca.nombre = nombre
    marca.urlLogo = urlLogo
    db.session.commit()
    return True

# ELIMINAR UNA MARCA POR IDMARCA
def eliminar_marca(idMarca):
    marca = Marca.query.get(idMarca)
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

