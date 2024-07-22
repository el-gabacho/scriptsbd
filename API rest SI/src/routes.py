from flask import Blueprint, request, jsonify
from models import db, MarcaSchema, Marca, Inventario, UnidadMedida, Proveedor, ProveedorProducto
from sqlalchemy.exc import ProgrammingError

routes = Blueprint('routes', __name__)

marca_schema = MarcaSchema()
marcas_schema = MarcaSchema(many=True)

@routes.route('/marcas', methods=['GET'])
def get_marcas():
    try:
        marcas = Marca.query.all()  # Obtener todas las marcas
        result = marcas_schema.dump(marcas)
        return jsonify(result)
    except ProgrammingError as e:
        return jsonify({'error': 'Error en la estructura de la base de datos', 'details': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Ocurrió un error inesperado', 'details': str(e)}), 500

@routes.route('/marcas/<int:id>', methods=['GET'])
def get_marca(id):
    try:
        marca = Marca.query.get(id)  # Obtener una marca específica
        if marca:
            result = marca_schema.dump(marca)
            return jsonify(result)
        return jsonify({'message': 'Marca no encontrada'}), 404
    except ProgrammingError as e:
        return jsonify({'error': 'Error en la estructura de la base de datos', 'details': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Ocurrió un error inesperado', 'details': str(e)}), 500


@routes.route('/info_productos', methods=['GET'])
def get_info_productos():
    try:
        productos = db.session.query(
            Inventario.idInventario,
            Inventario.codigoBarras,
            Inventario.nombre,
            Inventario.descripcion,
            Inventario.cantidadActual,
            Inventario.cantidadMinima,
            Inventario.precioCompra,
            Inventario.mayoreo,
            Inventario.menudeo,
            Inventario.colocado,
            Inventario.nombreImagen,
            UnidadMedida.tipoMedida,
            UnidadMedida.descripcion.label('unidadMedidaDescripcion'),
            Proveedor.empresa.label('proveedorEmpresa'),
            Proveedor.nombreEncargado.label('proveedorNombreEncargado'),
            Proveedor.telefono.label('proveedorTelefono'),
            Proveedor.correo.label('proveedorCorreo')
        ).join(
            UnidadMedida, Inventario.idUnidadMedida == UnidadMedida.idUnidadMedida
        ).join(
            ProveedorProducto, Inventario.idInventario == ProveedorProducto.idInventario
        ).join(
            Proveedor, ProveedorProducto.idProveedor == Proveedor.idProveedor
        ).all()

        productos_list = []
        for producto in productos:
            productos_list.append({
                'idInventario': producto.idInventario,
                'codigo': producto.codigoBarras,
                'NombreProducto': producto.nombre,
                'descripcion': producto.descripcion,
                'Existencias': producto.cantidadActual,
                'cantidadMinima': producto.cantidadMinima,
                'precioCompra': producto.precioCompra,
                'precioMayoreo': producto.mayoreo,
                 'precioMenudeo': producto.menudeo,
                'precioColocado': producto.colocado,
                'imagen': producto.nombreImagen,
                'tipoMedida': producto.tipoMedida,
                'unidadMedidaDescripcion': producto.unidadMedidaDescripcion,
                'proveedorEmpresa': producto.proveedorEmpresa,
                'Proveedor': producto.proveedorNombreEncargado,
            })

        return jsonify(productos_list)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@routes.route('/info_productos/<codigo_barras>', methods=['GET'])
def get_info_productos_by(codigo_barras):
    try:
        producto = db.session.query(
            Inventario.idInventario,
            Inventario.codigoBarras,
            Inventario.nombre,
            Inventario.descripcion,
            Inventario.cantidadActual,
            Inventario.cantidadMinima,
            Inventario.precioCompra,
            Inventario.mayoreo,
            Inventario.menudeo,
            Inventario.colocado,
            Inventario.nombreImagen,
            UnidadMedida.tipoMedida,
            UnidadMedida.descripcion.label('unidadMedidaDescripcion'),
            Proveedor.empresa.label('proveedorEmpresa'),
            Proveedor.nombreEncargado.label('proveedorNombreEncargado'),
            Proveedor.telefono.label('proveedorTelefono'),
            Proveedor.correo.label('proveedorCorreo')
        ).join(
            UnidadMedida, Inventario.idUnidadMedida == UnidadMedida.idUnidadMedida
        ).join(
            ProveedorProducto, Inventario.idInventario == ProveedorProducto.idInventario
        ).join(
            Proveedor, ProveedorProducto.idProveedor == Proveedor.idProveedor
        ).filter(
            Inventario.codigoBarras == codigo_barras
        ).first()

        if not producto:
            return jsonify({'message': 'Producto no encontrado'}), 404

        producto_data = {
            'idInventario': producto.idInventario,
            'codigoBarras': producto.codigoBarras,
            'producto': producto.nombre,
            'descripcion': producto.descripcion,
            'Existencias': producto.cantidadActual,
            'cantidadMinima': producto.cantidadMinima,
            'precioCompra': producto.precioCompra,
            'precioMayoreo': producto.mayoreo,
            'precioMenudeo': producto.menudeo,
            'precioColocado': producto.colocado,
            'imagen': producto.nombreImagen,
            'tipoMedida': producto.tipoMedida,
            'unidadMedidaDescripcion': producto.unidadMedidaDescripcion,
            'proveedorEmpresa': producto.proveedorEmpresa,
            'Proveedor': producto.proveedorNombreEncargado,
        }

        return jsonify(producto_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

