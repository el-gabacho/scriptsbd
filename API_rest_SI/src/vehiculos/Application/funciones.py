from init import db
from vehiculos.Domain.Marca import Marca, MarcaSchema
from vehiculos.Domain.Modelo import Modelo
from vehiculos.Domain.ModeloAnio import ModeloAnio
from vehiculos.Domain.Anio import Anio
from vehiculos.Domain.ModeloAutoparte import ModeloAutoparte
from inventario.Domain.Inventario import Inventario
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
        db.func.count(Modelo.idModelo).label('numeroModelos')
    ).outerjoin(
        Modelo, Marca.idMarca == Modelo.idMarca
    ).group_by(
        Marca.idMarca
    ).all()

    marcas_list = []
    for marca in marcas:
        marcas_list.append({
            'IdMarca': marca.idMarca,
            'Nombre': marca.nombre,
            'NumModelos': marca.numeroModelos,
        })

    return marcas_list

# -----------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------

# CRUD DE MARCA: BUSCAR POR NOMBRE DE LA MARCA, REALIZAR UN NUEVO MODELO, EDITAR MODELO Y ELIMINAR MODELO

def get_buscar_marcas_similar(nombremarca):
    marcas = db.session.query(
        Marca.idMarca,
        Marca.nombre,
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
            'IdMarca': marca.idMarca,
            'Nombre': marca.nombre,
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
    try:
        marca = Marca.query.get(idMarca)
        if not marca:
            return None, "Marca no encontrada"

        db.session.delete(marca)
        db.session.commit()
        return True
    except IntegrityError:
        db.session.rollback()
        return False

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
            'idMarca': resultado.idMarca,
            'idModelo': resultado.idModelo,
            'nombreModelo': resultado.nombreModelo,
            'numeroProductos': resultado.numeroProductos,
        })

    return modelos_list
# -----------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------

def obtener_marca(id):
    marca = Marca.query.get(id)
    print(marca)
    if marca:
        result = marca_schema.dump(marca)
        print(result)
        return result
    return None

# -----------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------

def obtener_modelo_anio_con_count(idmarca):
    query = db.session.query(
        ModeloAnio.idModeloAnio,
        Modelo.nombre,
        func.concat(
            func.coalesce(Anio.anioInicio, ''), '-', func.coalesce(Anio.anioFin, '')
        ).label('anioRango'),
        func.count(ModeloAutoparte.idInventario).label('numProductos')
    ).outerjoin(
        ModeloAnio, Modelo.idModelo == ModeloAnio.idModelo
    ).outerjoin(
        Anio, ModeloAnio.idAnio == Anio.idAnio
    ).outerjoin(
        ModeloAutoparte, ModeloAnio.idModeloAnio == ModeloAutoparte.idModeloAnio
    ).filter(
        Modelo.idMarca == idmarca
    ).group_by(
        Modelo.idModelo, ModeloAnio.idModeloAnio
    ).order_by(
        Modelo.nombre, ModeloAnio.idModeloAnio
    ).all()

    result = []
    for row in query:
        idModeloAnio = row.idModeloAnio if row.idModeloAnio else None
        result.append({
            'idModeloAnio': idModeloAnio,
            'nombre': row.nombre,
            'anioRango': row.anioRango,
            'numProductos': row.numProductos
        })

    return result

# -----------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------

def relaciona_modelo_anio(idModelo, anio_inicio, anio_fin, anio_todo):
    result = db.session.execute(f"CALL proc_modelo_anio({idModelo}, {anio_inicio}, {anio_fin}, {anio_todo})")
    errors = result.fetchall()
    return errors