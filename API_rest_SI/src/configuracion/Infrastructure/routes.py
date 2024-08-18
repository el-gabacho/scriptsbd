from flask import request, jsonify
from configuracion.Application.funciones import obtenerConfiguracion, actualizarConfiguracion, actualizarTelefonos, actualizarHorario
from configuracion import config as routes
from werkzeug.utils import secure_filename
import os

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
        return jsonify({'error': 'Error al actualizar la configuracion'}), 500

@routes.route('/configuracion/imagenes', methods=['POST'])
def upload_files():
    try:
        if 'files' not in request.files:
            return jsonify({'message': 'No file part in the request'}), 400

        files = request.files.getlist('files')

        for file in files:
            if file.filename == '':
                return jsonify({'message': 'No file selected for uploading'}), 400

            if file:
                filename = secure_filename(file.filename)
                file.save(os.path.join('C:\\Users\\VALENCIA\\Documents\\proyectos\\el-gabacho\\images', filename))
    except Exception as e:
        print(e)
        return jsonify({'message': 'Allowed file types are .webp'}), 400
    return jsonify({'message': 'Files successfully uploaded'}), 200