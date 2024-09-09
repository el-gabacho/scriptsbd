from mysql.connector import DatabaseError
import mysql.connector
import re
import time
from inflect import engine
import Levenshtein

cnx = mysql.connector.connect(user='root', password='root', host='localhost', port=3307, collation='utf8mb4_general_ci')

cursor = cnx.cursor()
errores_list = []
MAX_RETRIES = 3
p = engine()

cursor.execute("USE el_gabacho;")
cursor.execute("SELECT nombre FROM marcas;")
marcas = cursor.fetchall()
marcas = [marca[0] for marca in marcas]

cursor.execute("SELECT nombre FROM categorias;")
categorias = cursor.fetchall()
categorias = [categoria[0] for categoria in categorias]

cursor.execute("SELECT idProveedor, empresa FROM proveedores;")
proveedores = cursor.fetchall()

correcciones = {
    'RAV 4': 'RAV4',
    'PICK-UP': 'PICK UP',
    'CUTLAS': 'CUTLASS',
    'KODIAC': 'KODIAK',
    'F150': 'F-150',
    'PHATFINDER': 'PATHFINDER',
    'MITSUBICHI': 'MITSUBISHI',
    'VOLKSAWAGEN': 'VOLKSWAGEN',
    'SAMURAY': 'SAMURAI',
    'NV 200': 'NV200',
    'KENWOTH': 'KENWORTH',
}

# Expresión regular para extraer marca, modelo y año
marca_regex = re.compile(r'\b(' + '|'.join(marcas) + r')\b', re.IGNORECASE)
anio_regex = re.compile(r'\b((19[6-9]\d|20[0-2]\d)|(\d{2}|\d{4})\s*[-/]\s*(\d{2}|\d{4}))\b')
categoria_regex = re.compile(r'\b(' + '|'.join(categorias) + r')\b', re.IGNORECASE)

def migrate_and_cleanse_data():
    # Primera consulta
    cursor.execute("USE punto_venta;")
    cursor.execute("DELETE FROM tc_productos WHERE estatus=0 OR codigo_barras='';")
    cursor.execute("""
        DELETE p
        FROM tc_productos p
        JOIN (
            SELECT 
                codigo_barras,
                MIN(idproducto) AS id_min
            FROM tc_productos
            GROUP BY codigo_barras
        ) duplicados
        ON p.codigo_barras = duplicados.codigo_barras
        AND p.idproducto != duplicados.id_min;
    """)

    # Segunda consulta
    cursor.execute("USE el_gabacho;")
    cursor.execute("""
        CREATE TABLE tc_productos2 (
            id INT,
            codigo VARCHAR(120) NOT NULL,
            nombre VARCHAR(150) DEFAULT NULL,
            p_compra FLOAT DEFAULT 0.00,
            p_mayoreo FLOAT DEFAULT 0.00,
            p_llevar FLOAT DEFAULT 0.00,
            p_colocado FLOAT DEFAULT 0.00,
            existencia FLOAT DEFAULT 0.00,
            cantidad_minima INT DEFAULT 0,
            estatus INT DEFAULT 1,
            agranel VARCHAR(10) DEFAULT 'NO',
            proveedor VARCHAR(80) DEFAULT NULL
        );
    """)
    cursor.execute("""
        INSERT INTO tc_productos2 (id, codigo, nombre, p_compra, p_mayoreo, p_llevar, p_colocado, existencia, cantidad_minima, estatus, agranel, proveedor)
        SELECT idproducto, codigo_barras, nombre_producto, precio_compra, precio_venta, precio2, precio3, existencia, cantidad_minima, estatus, agranel, campo2 
        FROM punto_venta.tc_productos;
    """)

def obtener_id(id_columna, tabla, columna, valor):
    """Obtener ID genérico de una tabla dada."""
    cursor.execute(f"SELECT {id_columna} FROM {tabla} WHERE {columna} = %s", (valor,))
    resultado = cursor.fetchone()
    return resultado[0] if resultado else None

def obtener_modelos_de_marca(marca):
    cursor.execute(f"SELECT idMarca FROM marcas WHERE nombre = '{marca}';")
    id_marca = cursor.fetchone()[0]
    cursor.execute(f"SELECT nombre FROM modelos WHERE idMarca = {id_marca};")
    modelos = cursor.fetchall()
    modelos = [modelo[0] for modelo in modelos]
    return modelos

def obtener_id_modelo(nombre_modelo, nombre_marca):
    cursor.execute(f"SELECT mo.idModelo FROM modelos mo JOIN marcas ma ON mo.idMarca = ma.idMarca WHERE mo.nombre = '{nombre_modelo}' AND ma.nombre='{nombre_marca}';")
    id_modelo = cursor.fetchone()[0]
    return id_modelo

def validate_anio(anio):
    converted_year = ''
    year2 = anio.split('-')
    for y in year2:
        if len(y) == 2:
            start_digit = int(y[0])
            if start_digit >= 5:
                converted_year += '19' + y + '-'
            else:
                converted_year += '20' + y + '-'
    return converted_year[:-1]

def manejar_error(fila, mensaje):
    """Agregar error a la lista de errores."""
    errores_list.append({'Fila': fila, 'Mensaje': mensaje})
    
def eliminar_info_vehiculo(nombre, vehiculos):
    for vehiculo in vehiculos:
        nombre = nombre.replace(vehiculo['marca'], '')
        nombre = nombre.replace(vehiculo['modelo'], '')
        nombre = nombre.replace(vehiculo['anio'], '')
    return nombre.strip()

def encontrar_proveedor_cercano(proveedor):
    for id_proveedor, nombre in proveedores:
        if Levenshtein.distance(proveedor, nombre) <= 1:
            return id_proveedor
    return 0

def extraer_categoria(nombre):
    palabras = nombre.split()
    for palabra in palabras:
        singular = p.plural_noun(palabra)
        if singular in categorias:
            return singular
        if palabra in categorias:
            return palabra
    return None

def extraer_vehiculos(nombre):
    
    vehiculos = []
    # Aplicar las correcciones al nombre
    for mal_escrito, correccion in correcciones.items():
        nombre = nombre.replace(mal_escrito, correccion)
    marcas_encontradas = marca_regex.findall(nombre)
    anio_match = anio_regex.search(nombre)
    anio = anio_match.group(0) if anio_match else None


    for i, marca in enumerate(marcas_encontradas):
        marca = marca.upper()
        modelos_marca = obtener_modelos_de_marca(marca)
        modelo_regex = re.compile(r'\b(' + '|'.join(modelos_marca) + r')\b', re.IGNORECASE)

        # Determinar el final de la sección para esta marca
        if i < len(marcas_encontradas) - 1:
            fin_seccion = nombre.index(marcas_encontradas[i+1])
        else:
            fin_seccion = len(nombre)

        # Buscar todos los modelos en la sección para esta marca
        seccion = nombre[:fin_seccion]
        modelos = modelo_regex.findall(seccion)

        # Crear la lista de vehículos para esta marca
        for modelo in modelos:
            converted_year = ''
            if isinstance(modelo, tuple):
                modelo = modelo[0]
            
            if not anio:
                converted_year = "ALL YEARS"
            elif re.match(r'^(\d{2})\s*[-]\s*(\d{2})$', anio):
                converted_year = anio.replace('- ', '-')
                converted_year = validate_anio(converted_year)
                if re.match(r'^\d{4}$', converted_year):
                    converted_year = f"{converted_year}-{converted_year}"
            elif re.match(r'^(\d{4})\s*[-]\s*(\d{4})$', anio):
                converted_year = anio.replace('- ', '-')
                converted_year = anio
            elif re.match(r'^\d{4}$', anio):
                converted_year = f"{anio}-{anio}"
            elif re.match(r'^(\d{4})\s*[/]\s*(\d{4})$', anio):
                converted_year = anio.replace(' / ', '-')
                converted_year = anio.replace('/', '-')
            elif re.match(r'^(\d{2})\s*[/]\s*(\d{2})$', anio):
                converted_year = anio.replace(' / ', '-')
                converted_year = anio.replace('/', '-')
                converted_year = validate_anio(converted_year)
            vehiculos.append({"marca": marca, "modelo": modelo.upper(), "anio": converted_year})

        # Eliminar la sección procesada del nombre
        nombre = nombre[fin_seccion:]

    return vehiculos

def obtener_productos():
    productos_list = []
    producto_dict = {}
    descripcion = ""
    cursor.execute("SELECT id, codigo, nombre, p_compra, p_mayoreo, p_llevar, p_colocado, existencia, cantidad_minima, agranel, proveedor FROM tc_productos2;")
    productos = cursor.fetchall()

    for producto in productos:
        vehiculos = extraer_vehiculos(producto[2])
        if vehiculos:
            descripcion = eliminar_info_vehiculo(producto[2], vehiculos)
        else:
            descripcion = producto[2]
            
        categoria = extraer_categoria(producto[2])
        if not categoria:
            categoria = "VARIOS"
            
        producto_dict = {
            "fila": producto[0],
            "CODIGO": producto[1],
            "NOMBRE": descripcion.split()[0],
            "DESCRIPCION": descripcion,
            "COMPRA": producto[3],
            "MAYOREO": producto[4],
            "LLEVAR": producto[5],
            "COLOCADO": producto[6],
            "EXISTENCIAS": producto[7],
            "CANT_MIN": producto[8],
            "TIPO_MED": producto[9],
            "PROVEEDOR": producto[10],
            "CATEGORIA": categoria,
            "vehiculos": vehiculos
        }
        productos_list.append(producto_dict)

    return productos_list

def obtener_ids_modelo_anios(fila, vehiculos):
    """Obtener IDs de ModeloAnios para una lista de vehículos."""
    id_modelo_anios_list  = []
    for vehiculo in vehiculos:
        idModelo = obtener_id_modelo(vehiculo['modelo'], vehiculo['marca'])

        if idModelo is None:
            manejar_error(fila, f"No se encontró idModelo con el modelo {vehiculo['modelo']}")
            continue

        if not vehiculo['anio'] or vehiculo['anio'] == '' or vehiculo['anio'] == 'ALL YEARS':
            try:
                result_args = cursor.callproc('proc_insertar_modelos', [idModelo, 0, 0, True, 0])
            except mysql.connector.DatabaseError as e:
                manejar_error(fila, str(e))
                continue
        else:
            anios = vehiculo['anio'].split('-')
            try:
                result_args = cursor.callproc('proc_insertar_modelos', [idModelo, anios[0], anios[1], False, 0])
            except mysql.connector.DatabaseError as e:
                manejar_error(fila, str(e))
                continue
            
        idModeloAnio = result_args[-1]
        id_modelo_anios_list.append(str(idModeloAnio))

    return ','.join(id_modelo_anios_list) if id_modelo_anios_list else None

def procesar_producto(producto):
    
    actualizado = False
    registrado = False
    """Procesa un solo producto, actualizándolo o insertándolo según corresponda."""
    id_categoria = obtener_id('idCategoria','categorias', 'nombre', producto['CATEGORIA'])
    if id_categoria is None:
        manejar_error(producto['fila'], f"No se encontró idCategoria con la categoría {producto['CATEGORIA']}")
        return None, None

    id_proveedor = encontrar_proveedor_cercano(producto['PROVEEDOR'])

    id_unidad_medida = {'NO': 1, 'SI': 2}.get(producto['TIPO_MED'])
    if id_unidad_medida is None:
        manejar_error(producto['fila'], 'Valor inválido para TIPO_MED')
        return None, None

    existencias = producto['EXISTENCIAS']
    if existencias < 0:
        existencias = 0
    id_inventario = obtener_id('idInventario','inventario', 'codigoBarras', producto['CODIGO'])
    
    cantidadMinima = producto['CANT_MIN']
    if not cantidadMinima:
        cantidadMinima = 0
    
    if id_inventario:
        try:
            cursor.callproc('proc_actualizar_producto_con_comparacion', [id_inventario, id_categoria, id_unidad_medida, producto['CODIGO'] , producto['NOMBRE'], producto['DESCRIPCION'], existencias, cantidadMinima, producto['COMPRA'], producto['MAYOREO'], producto['LLEVAR'], producto['COLOCADO'], id_proveedor])
            actualizado = True
        except DatabaseError  as e:
            manejar_error(producto['fila'], str(e))
            return None, None
        
        id_modelo_anios_string = obtener_ids_modelo_anios(producto['fila'], producto['vehiculos'])
        if id_modelo_anios_string is None:
            manejar_error(producto['fila'], 'No se generó ningún idModeloAnio')
            return actualizado, None

        try:
            cursor.callproc('proc_editar_producto_modeloanios', (id_inventario, id_modelo_anios_string))
        except DatabaseError as e:
            manejar_error(producto['fila'], str(e))
            return actualizado, None
        
        return actualizado, registrado
    else:
        params = [id_categoria, id_unidad_medida, producto['CODIGO'], producto['NOMBRE'], producto['DESCRIPCION'], existencias, cantidadMinima, producto['COMPRA'], producto['MAYOREO'], producto['LLEVAR'], producto['COLOCADO'], id_proveedor, 1, 0]
        for i in range(MAX_RETRIES):
            try:
                result_args = cursor.callproc('proc_insertar_producto', params)
                id_inventario = result_args[-1]
                registrado = True
                break
            except DatabaseError  as e:
                if 'Lock wait timeout exceeded' in str(e):
                    time.sleep(5)
                else:
                    manejar_error(producto['fila'], str(e))
                    return None, None

        if id_inventario == 0:
            manejar_error(producto['fila'], 'No se generó el idInventario')
            return None, None
        
        id_modelo_anios_string = obtener_ids_modelo_anios(producto['fila'], producto['vehiculos'])
        if id_modelo_anios_string is None:
            # manejar_error(producto['fila'], 'No se generó ningún idModeloAnio')
            return None, registrado

        try:
            cursor.callproc('proc_relate_producto_modeloanios', (id_inventario, id_modelo_anios_string))
        except DatabaseError as e:
            manejar_error(producto['fila'], str(e))
            return None, registrado
        
        return actualizado, registrado
    
# Contadores para productos insertados y actualizados
total_insertados = 0
total_actualizados = 0
try:
    migrate_and_cleanse_data()
    productos_list = obtener_productos()

    # Procesar cada producto en la lista de productos
    for producto in productos_list:
        actualizado, registrado = procesar_producto(producto)
        if actualizado is None and registrado is None:
            continue
        if actualizado:
            total_actualizados += 1
        elif registrado:
            total_insertados += 1

    # Confirmar los cambiosx
    cnx.commit()
finally:
    # Cerrar el cursor y la conexión
    cursor.close()
    cnx.close()

errores_list.sort(key=lambda x: x['Fila'])
resultado = {'TotalInsertados': total_insertados, 'TotalActualizados': total_actualizados, 'Errores': errores_list}
print(resultado)