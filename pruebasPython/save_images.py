import mysql.connector
from PIL import Image
import io
import os

# Conectar a la base de datos
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='punto_venta'
)

# Crear un cursor
cursor = conn.cursor()

# Crear una carpeta para guardar las imágenes si no existe
if not os.path.exists('images'):
    os.makedirs('images')

# Tamaño del lote
batch_size = 100

# Obtener el número total de registros
cursor.execute("SELECT COUNT(*) FROM tc_productos WHERE imagen != ''")
total_records = cursor.fetchone()[0]
print(f'Total de imágenes a procesar: {total_records}')

# Número de lotes
num_batches = (total_records // batch_size) + 1

for batch in range(num_batches):
    offset = batch * batch_size
    print(f'Procesando lote {batch + 1} de {num_batches}, registros {offset + 1} a {offset + batch_size}')
    
    # Ejecutar la consulta para obtener un lote de BLOBs que no están vacíos
    cursor.execute(f"SELECT idproducto, imagen FROM tc_productos WHERE imagen != '' LIMIT {batch_size} OFFSET {offset}")
    records = cursor.fetchall()
    
    # Procesar cada registro en el lote
    for record in records:
        idproducto = record[0]
        imagen_blob = record[1]
        
        # Convertir los datos binarios a una imagen
        image = Image.open(io.BytesIO(imagen_blob))
        
        # Guardar la imagen en formato WebP
        image.save(f'images/{idproducto}.webp', 'webp')
        
        # Liberar la memoria de la imagen
        image.close()

# Cerrar el cursor y la conexión
cursor.close()
conn.close()

print("Imágenes guardadas exitosamente en formato WebP.")