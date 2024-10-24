from flask import request, jsonify
from configuracion.funciones import obtenerConfiguracion, actualizarConfiguracion, actualizarTelefonos, actualizarHorario
from configuracion import config as routes
from werkzeug.utils import secure_filename
import os
from config import IMAGE_ROOT_PATH

@routes.route('/configuracion', methods=['GET'])
def getConfiguracion():
    try:
        resultado = obtenerConfiguracion()
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'error': 'Ocurrió un problema al obtener la configuracion. Por favor, inténtalo más tarde.'}), 500
    
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
        return jsonify({'error': 'Hubo un problema al actualizar la configuracion. Verifica su servidor y notifique al administrador.'}), 500

@routes.route('/configuracion/imagenes', methods=['POST'])
def upload_files():
    try:
        if 'files' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400

        files = request.files.getlist('files')

        for file in files:
            if file.filename == '':
                return jsonify({'error': 'No file selected for uploading'}), 400

            if file:
                filename = secure_filename(file.filename)
                if filename.split('.')[-1] != 'webp':
                    return jsonify({'error': 'Allowed file types are .webp'}), 400
                if filename == 'logo.webp':
                    file.save(os.path.join(IMAGE_ROOT_PATH, filename))
                else:
                    file.save(os.path.join(f"{IMAGE_ROOT_PATH}/carrrusel", filename))
        return jsonify({'message': 'Files successfully uploaded'}), 200
            
    except Exception as e:
        return jsonify({'error': 'Allowed file types are .webp'}), 400