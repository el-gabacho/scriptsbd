from configuracion.modelos import Configuracion, Horario, TelefonosEmpresa
from init import db

def obtenerConfiguracion():
    # Consulta para obtener los datos de telefonos de la empresa
    telefonos = TelefonosEmpresa.query.with_entities(TelefonosEmpresa.idTelefono, TelefonosEmpresa.numero, TelefonosEmpresa.tipo).all()
    
    # Consulta para obtener los datos de configuracion
    config = Configuracion.query.with_entities(Configuracion.correo, Configuracion.direccion, Configuracion.encabezado, Configuracion.footer).first()
    
    # Consulta para obtener los datos de horario
    horarios = Horario.query.with_entities(Horario.idDia, Horario.dias, Horario.horaInicio, Horario.horaFin).all()
    
    # Crear el diccionario con los resultados
    resultado = {
        'Telefonos': [{'Id': telefono.idTelefono, 'Numero': telefono.numero, 'Tipo': telefono.tipo} for telefono in telefonos],
        'Configuracion': {
            'Correo': config.correo,
            'Direccion': config.direccion,
            'Encabezado': config.encabezado,
            'Footer': config.footer
        },
        'Horarios': [{'Id': horario.idDia, 'Dias': horario.dias, 'HoraInicio': horario.horaInicio, 'HoraFin': horario.horaFin} for horario in horarios]
    }
    
    return resultado

def actualizarConfiguracion(correo, direccion, encabezado, footer):
    print(correo)
    print(direccion)
    print(encabezado)
    print(footer)
    # Consulta para obtener los datos de configuracion
    config = Configuracion.query.get(1)
    
    # Verificar si el registro existe
    if config is None:
        return {'message': 'No se encontró la configuración'}
    
    # Actualizar los datos de configuracion
    config.correo = correo
    config.direccion = direccion
    config.encabezado = encabezado
    config.footer = footer
    
    # Guardar los cambios en la base de datos
    db.session.commit()
    
    return {'message': 'Configuracion actualizada correctamente'}

def actualizarTelefonos(telefonos):
    # Consulta para obtener los datos de telefonos de la empresa
    telefonos_db = TelefonosEmpresa.query.all()
    
    # Actualizar los telefonos existentes en la base de datos
    for telefono in telefonos_db:
        for nuevo_telefono in telefonos:
            if telefono.idTelefono == nuevo_telefono['id']:
                telefono.numero = nuevo_telefono['numero']
                telefono.tipo = nuevo_telefono['tipo']
                break
    
    # Guardar los cambios en la base de datos
    db.session.commit()
    
    return {'message': 'Telefonos actualizados correctamente'}

def actualizarHorario(horarios):
    # Consulta para obtener los datos de horario
    horarios_db = Horario.query.all()
    
    # Actualizar los horarios existentes en la base de datos
    for horario_db in horarios_db:
        for horario in horarios:
            if horario_db.idDia == horario['id']:
                horario_db.dias = horario['dias']
                horario_db.horaInicio = horario['horaInicio']
                horario_db.horaFin = horario['horaFin']
                break
        else:
            # Si no se encuentra el horario en la base de datos, crear uno nuevo
            nuevo_horario = Horario(dias=horario['dias'], horaInicio=horario['horaInicio'], horaFin=horario['horaFin'])
            db.session.add(nuevo_horario)
    
    # Guardar los cambios en la base de datos
    db.session.commit()
    
    return {'message': 'Horario actualizado correctamente'}