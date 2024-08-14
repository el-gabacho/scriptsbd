from flask import request, jsonify
from configuracion.Application.funciones import obtenerConfiguracion, actualizarConfiguracion, actualizarTelefonos, actualizarHorario
from configuracion import config as routes

@routes.route('/configuracion', methods=['GET'])
def getConfiguracion():
    try:
        resultado = obtenerConfiguracion()
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'error': 'Error al obtener la configuracion'}), 500
    
@routes.route('/configuracion', methods=['PUT'])
def updateConfiguracion():
    try:
        resultados = []
        data = request.get_json()
        configuracion = data.get('configuracion')
        telefonos = data.get('telefonos')
        horarios = data.get('horarios')
        
        resultados.append(actualizarConfiguracion(configuracion['correo'], configuracion['direccion'], configuracion['encabezado'], configuracion['footer']))
        resultados.append(actualizarTelefonos(telefonos))
        resultados.append(actualizarHorario(horarios))
        
        return jsonify(resultados)
    except Exception as e:
        print(e)
        return jsonify({'error': 'Error al actualizar la configuracion'}), 500