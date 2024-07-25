from models import db, Marca, Modelo, ModeloAnio, ModeloAutoparte, Anio
from sqlalchemy import func

def get_marcas_con_count_modelos():
    marcas = db.session.query(
        Marca.idMarca,
        Marca.nombre,
        db.func.count(Modelo.nombre)
    ).join(
        Modelo, Marca.idMarca == Modelo.idMarca
    ).group_by(
        Marca.idMarca
    ).all()

    marcas_list = []
    for marca in marcas:
        marcas_list.append({
            'idMarca': marca.idMarca,
            'nombre': marca.nombre,
            'count': marca[2]
        })

    return marcas_list

def get_marca(id):
    marca = Marca.query.get(id)
    if marca:
        return marca
    return None

def get_modelo_anio_count(idmarca):
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

def relaciona_modelo_anio(idModelo, anio_inicio, anio_fin, anio_todo):
    result = db.session.execute(f"CALL proc_modelo_anio({idModelo}, {anio_inicio}, {anio_fin}, {anio_todo})")
    errors = result.fetchall()
    return errors