import pandas as pd
import re
import time
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from init import db
from vehiculos.funciones import obtener_id_marca, obtener_id_modelo, obtener_id_anio, obtener_id_modelo_anio
from inventario.funciones import obtener_id_inventario
from categorias.funciones import obtener_id_categoria

MAX_RETRIES = 3

errores_list = []

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
    
def obtener_ids_modelo_anios(fila, vehiculos):
    """Obtener IDs de ModeloAnios para una lista de vehículos."""
    id_modelo_anios_list  = []
    for vehiculo in vehiculos:
        id_marca = obtener_id_marca(vehiculo['marca'])        
        if id_marca is None:
            manejar_error(fila, f"No se encontró idMarca con la marca {vehiculo['marca']}")
            continue

        idModelo = obtener_id_modelo(id_marca, vehiculo['modelo'])

        if idModelo is None:
            manejar_error(fila, f"No se encontró idModelo con el modelo {vehiculo['modelo']}")
            continue

        anios = vehiculo['anio'].split('-')
        idAnio = obtener_id_anio(anios[0], anios[1])
        if idAnio is None:
            manejar_error(fila, f'No se encontró idAnio con el año {vehiculo["anio"]}')
            continue

        idModeloAnio = obtener_id_modelo_anio(idModelo, idAnio)
        if idModeloAnio is None:
            try:
                db.session.execute(text(f"CALL proc_insertar_modelos({idModelo}, {anios[0]}, {anios[1]}, False, @idModeloAnio)"))
                idModeloAnio = db.session.execute(text("SELECT @idModeloAnio")).scalar()
            except SQLAlchemyError as e:
                manejar_error(fila, str(e))
                continue
            except Exception as e:
                manejar_error(fila, str(e))
                continue
            
        id_modelo_anios_list.append(str(idModeloAnio))

    return ','.join(id_modelo_anios_list) if id_modelo_anios_list else None

def procesar_producto(producto, usuarioId):
    from proveedores.funciones import obtener_id_proveedor
    
    actualizado = False
    registrado = False
    """Procesa un solo producto, actualizándolo o insertándolo según corresponda."""
    id_categoria = obtener_id_categoria(producto['CATEGORIA'])
    if id_categoria is None:
        manejar_error(producto['fila'], f"No se encontró idCategoria con la categoría {producto['CATEGORIA']}")
        return None, None

    id_proveedor = obtener_id_proveedor(producto['PROVEEDOR'])
    if id_proveedor is None:
        manejar_error(producto['fila'], f"No se encontró idProveedor con el proveedor {producto['PROVEEDOR']}")
        return None, None

    id_unidad_medida = {'PZA': 1, 'M': 2}.get(producto['TIPO_MED'])
    if id_unidad_medida is None:
        manejar_error(producto['fila'], 'Valor inválido para TIPO_MED')
        return None, None

    id_inventario = obtener_id_inventario(producto['CODIGO'])
    
    if id_inventario:
        try:
            db.session.execute(text(f"CALL proc_actualizar_producto_con_comparacion({id_inventario}, {id_categoria}, {id_unidad_medida}, '{producto['NOMBRE']}', '{producto['DESCRIPCION']}', {producto['EXISTENCIAS']}, {producto['CANT_MIN']}, {producto['COMPRA']}, {producto['MAYOREO']}, {producto['LLEVAR']}, {producto['COLOCADO']}, {id_proveedor})"))
            actualizado = True
        except SQLAlchemyError as e:
            manejar_error(producto['fila'], str(e))
            return None, None
        
        id_modelo_anios_string = obtener_ids_modelo_anios(producto['fila'], producto['vehiculos'])
        if id_modelo_anios_string is None:
            manejar_error(producto['fila'], 'No se generó ningún idModeloAnio')
            return actualizado, None

        try:
            db.session.execute(text(f"CALL proc_editar_producto_modeloanios({id_inventario}, '{id_modelo_anios_string}')"))
        except SQLAlchemyError as e:
            manejar_error(producto['fila'], str(e))
            return actualizado, None
        
        return actualizado, registrado
    else:
        for i in range(MAX_RETRIES):
            try:
                db.session.execute(text(f"CALL proc_insertar_producto({id_categoria}, {id_unidad_medida}, '{producto['CODIGO']}', '{producto['NOMBRE']}', '{producto['DESCRIPCION']}', {producto['EXISTENCIAS']}, {producto['CANT_MIN']}, {producto['COMPRA']}, {producto['MAYOREO']}, {producto['LLEVAR']}, {producto['COLOCADO']}, {id_proveedor}, {usuarioId}, @id_inventario)"))
                id_inventario = db.session.execute(text("SELECT @id_inventario")).scalar()
                registrado = True
                break
            except SQLAlchemyError as e:
                if 'Lock wait timeout exceeded' in str(e):
                    time.sleep(5)
                else:
                    manejar_error(producto['fila'], str(e))
                    return

        if id_inventario == 0:
            manejar_error(producto['fila'], 'No se generó el idInventario')
            return None, None
        
        id_modelo_anios_string = obtener_ids_modelo_anios(producto['fila'], producto['vehiculos'])
        if id_modelo_anios_string is None:
            manejar_error(producto['fila'], 'No se generó ningún idModeloAnio')
            return None, registrado

        try:
            db.session.execute(text(f"CALL proc_relate_producto_modeloanios({id_inventario}, {id_modelo_anios_string})"))
        except SQLAlchemyError as e:
            manejar_error(producto['fila'], str(e))
            return None, registrado
        
        return actualizado, registrado
    
def procesar_csv(file_path):
    df = pd.read_csv(file_path)
    productos_list = []

    # Check for missing values in the required columns
    required_columns = ['CODIGO', 'NOMBRE', 'EXISTENCIAS', 'PROVEEDOR', 'CATEGORIA', 'MARCA1', 'MODELO1', 'ANIO1']
    missing_values = df[required_columns].isnull().any(axis=1)

    # Store the rows with errors in the errores variable
    filtered_df = df[~missing_values]

    # Iterate over the missing values and create error dictionaries
    for index, row in df[missing_values].iterrows():
        for column in required_columns:
            if pd.isnull(row[column]):
                manejar_error(index, f"La columna {column} está vacía")
                break
        
    # Check and convert the columns COMPRA, MAYOREO, LLEVAR, COLOCADO
    for column in ['COMPRA', 'MAYOREO', 'LLEVAR', 'COLOCADO']:
        # Remove the $ symbol and commas, and convert to float
        filtered_df.loc[:, column] = filtered_df[column].replace({'\$': '', ',': ''}, regex=True)
        
        # Check if the column contains non-numeric values
        non_numeric_values = pd.to_numeric(filtered_df[column], errors='coerce').isna()
        
        # Convert the column to numeric, setting non-numeric values to NaN
        filtered_df.loc[:, column] = pd.to_numeric(filtered_df[column], errors='coerce')
        
        # Replace NaN values with 0
        filtered_df.loc[:, column] = filtered_df[column].fillna(0)
        
        # Store the rows with non-numeric values in the errores_list
        error_rows = filtered_df[non_numeric_values].index.tolist()
        for row in error_rows:
            manejar_error(row, f"La columna {column} tiene valores no numéricos o esta vacio")
            
    # Convert EXISTENCIAS and CANT_MIN to float and handle NaN values
    filtered_df.loc[:, 'EXISTENCIAS'] = pd.to_numeric(filtered_df['EXISTENCIAS'], errors='coerce').fillna(0)
    filtered_df.loc[:, 'CANT_MIN'] = pd.to_numeric(filtered_df['CANT_MIN'], errors='coerce').fillna(0)

    # Convert TIPO_MED, PROVEEDOR, CATEGORIA, MARCA1, MODELO1 to uppercase
    filtered_df.loc[:, 'TIPO_MED'] = filtered_df['TIPO_MED'].str.upper()
    filtered_df.loc[:, 'PROVEEDOR'] = filtered_df['PROVEEDOR'].str.upper()
    filtered_df.loc[:, 'CATEGORIA'] = filtered_df['CATEGORIA'].str.upper()
    filtered_df.loc[:, 'MARCA1'] = filtered_df['MARCA1'].str.upper()
    filtered_df.loc[:, 'MODELO1'] = filtered_df['MODELO1'].str.upper()

    # Check and validate values in TIPO_MED column
    invalid_tipo_med = ~filtered_df['TIPO_MED'].isin(['PZA', 'M'])
    for row in invalid_tipo_med[invalid_tipo_med].index:
        manejar_error(row, f"La columna TIPO_MED tiene un valor inválido")
    filtered_df = filtered_df[~invalid_tipo_med]

    # Check and validate values in ANIO1 column
    invalid_anio1 = ~filtered_df['ANIO1'].str.match(r'^\d{2}-\d{2}$') & ~filtered_df['ANIO1'].str.match(r'^\d{4}-\d{4}$')
    for row in invalid_anio1[invalid_anio1].index:
        manejar_error(row, f"La columna ANIO1 tiene un valor inválido")
    filtered_df = filtered_df[~invalid_anio1]
    
    # Iterate over each row of the filtered_df dataframe
    for index, row in filtered_df.iterrows():
        vehiculos = []
        
        # Iterate over the different sets of columns
        for i in range(1, 6):
            marca_col = f'MARCA{i}'
            modelo_col = f'MODELO{i}'
            anio_col = f'ANIO{i}'
            
            # Check if the columns are not empty or NaN
            if not pd.isnull(row[marca_col]) and not pd.isnull(row[modelo_col]) and not pd.isnull(row[anio_col]):
                anio = str(row[anio_col]).strip()
                if re.match(r'^\d{2}-\d{2}$', anio):
                    converted_year = validate_anio(anio)
                    vehiculos.append({'marca': row[marca_col], 'modelo': row[modelo_col], 'anio': converted_year})
                elif re.match(r'^\d{4}-\d{4}$', anio):
                    vehiculos.append({'marca': row[marca_col], 'modelo': row[modelo_col], 'anio': anio})
                else:
                    manejar_error(index, f'La columna {anio_col} tiene un valor inválido')
            elif pd.isnull(row[marca_col]) and pd.isnull(row[modelo_col]) and pd.isnull(row[anio_col]):
                None
            else:
                manejar_error(index, f'Las columnas {marca_col}, {modelo_col} y {anio_col} deben estar llenas o vacías')
        
        # Add the vehicles to the vehiculos_list if any were found
        if vehiculos:
            productos_list.append({'fila': index, 'vehiculos': vehiculos})
            
    for index, row in filtered_df.iterrows():
        for producto in productos_list:
            if index == producto['fila']:
                for column in ['CODIGO', 'NOMBRE', 'DESCRIPCION', 'COMPRA', 'MAYOREO', 'LLEVAR', 'COLOCADO', 'EXISTENCIAS', 'CANT_MIN', 'TIPO_MED', 'PROVEEDOR', 'CATEGORIA']:
                    producto[column] = row[column]
                producto['vehiculos'] = producto['vehiculos']
                
    return productos_list
                
def importar_productos(file_path, usuarioId):
    # Contadores para productos insertados y actualizados
    total_insertados = 0
    total_actualizados = 0
    try:
        productos_list = procesar_csv(file_path)

        # Procesar cada producto en la lista de productos
        for producto in productos_list:
            actualizado, registrado = procesar_producto(producto, usuarioId)
            if actualizado is None and registrado is None:
                continue
            if actualizado:
                total_actualizados += 1
            elif registrado:
                total_insertados += 1

        # Confirmar los cambiosx
        db.session.commit()
    finally:
        db.session.close()

    errores_list = [{'Fila': x['Fila'] + 2} if 'Fila' in x else x for x in errores_list]
    errores_list.sort(key=lambda x: x['Fila'])
    resultado = {'TotalInsertados': total_insertados, 'TotalActualizados': total_actualizados, 'Errores': errores_list}
    return resultado