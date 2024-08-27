from flask import jsonify, request
from inventario.funciones import get_productos, get_producto_preciso, get_productos_similares
from inventario import inventory as routes

# TODOS LOS PRODUCTOS CON INFORMACION
@routes.route('/productos', methods=['GET', 'POST'])
def get_info_productos():
    try:
        data = request.get_json()
        idMarca = data.get('idMarca')
        idModelo = data.get('idModelo')
        anio = data.get('anio')
        anioInicio = anio.split('-')[0] if anio else None
        anioFin = anio.split('-')[1] if anio else None
        print(idMarca, idModelo, anioInicio, anioFin)
        productos = get_productos(idMarca, idModelo, anioInicio, anioFin)
        return jsonify(productos)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# UN PRODUCTO CON TODA INFORMACION CON CODIGO FIJO
@routes.route('/productos/<codigo_barras>', methods=['GET'])
def get_info_productos_preciso_by(codigo_barras):
    try:
        producto_preciso = get_producto_preciso(codigo_barras)
        return jsonify(producto_preciso)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# TODOS LOS PRODUCTOS CON INFORMACION CON CODIGO SIMILAR
@routes.route('/productos_simi', methods=['GET'])
def get_info_productos_similar_by():
    try:
        search = request.args.get('search')
        # Obtén los productos similares
        producto_similar = get_productos_similares(search)
        
        # Devuelve una lista vacía si no se encuentran productos similares
        if producto_similar is None or len(producto_similar) == 0:
            return jsonify([])

        # Devuelve la lista de productos similares
        return jsonify(producto_similar)
    except Exception as e:
        return jsonify({'error': str(e)}), 500