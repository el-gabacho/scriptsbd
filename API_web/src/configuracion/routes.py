from flask import jsonify
from configuracion.funciones import obtener_configuracion, obtener_telefonos, obtener_horario
from configuracion import config as routes

@routes.route('/configuracion', methods=['GET'])
def getConfiguracion():
    try:
        resultado = obtener_configuracion()
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'error': 'Error al obtener la configuracion','detalles':str(e)}), 500
    
@routes.route('/configuracion/telefonos', methods=['GET'])
def getTelefonos():
    try:
        resultado = obtener_telefonos()
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'error': 'Error al obtener los telefonos'}), 500
    
@routes.route('/configuracion/horario', methods=['GET'])
def getHorario():
    try:
        resultado = obtener_horario()
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'error': 'Error al obtener el horario'}), 500