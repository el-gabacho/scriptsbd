from configuracion.modelos import TelefonosEmpresa, Configuracion, Horario

def obtener_telefonos():
    telefonos = TelefonosEmpresa.query.all()
    telefonos_json = []
    for telefono in telefonos:
        telefono_json = {
            "numero": telefono.numero,
            "tipo": telefono.tipo
        }
        telefonos_json.append(telefono_json)
    return telefonos_json

def obtener_horario():
    horarios = Horario.query.all()
    horarios_json = []
    for horario in horarios:
        horario_json = {
            "dias": horario.dias,
            "horaInicio": horario.horaInicio,
            "horaFin": horario.horaFin
        }
        horarios_json.append(horario_json)
    return horarios_json

def obtener_configuracion():
    configuracion = Configuracion.query.first()
    if configuracion:
        configuracion_json = {
            "correo": configuracion.correo,
            "direccion": configuracion.direccion
        }
        return configuracion_json
    else:
        return None
