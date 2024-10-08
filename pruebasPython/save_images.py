import mysql.connector
from PIL import Image
import io

# Conectar a la base de datos
conn = mysql.connector.connect(
    host='localhost', port=3306,
    user='admin',
    password='admin123',
    database='punto_venta', collation='utf8mb4_general_ci'
)
IMAGE_ROOT_PATH = "/home/soygabacho/imagenes/productos/"

# Crear un cursor
cursor = conn.cursor()

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
    cursor.execute(f"SELECT codigo_barras, imagen FROM tc_productos WHERE imagen != '' LIMIT {batch_size} OFFSET {offset}")
    records = cursor.fetchall()
    
    # Procesar cada registro en el lote
    for record in records:
        codigo_barras = record[0]
        imagen_blob = record[1]
        
        # Convertir los datos binarios a una imagen
        image = Image.open(io.BytesIO(imagen_blob))
        
        # Guardar la imagen en formato WebP
        image.save(f'{IMAGE_ROOT_PATH}{codigo_barras}_1.webp', 'webp')
        
        # Liberar la memoria de la imagen
        image.close()

cursor.execute("""
    INSERT INTO imagenes (idInventario, imgRepresentativa)
    SELECT p1.idInventario, true
    FROM inventario p1
    JOIN punto_venta.tc_productos p2 ON p1.codigoBarras = p2.codigo_barras
    WHERE p2.imagen IS NOT NULL;
""")

# Cerrar el cursor y la conexión
cursor.close()
conn.close()

print("Imágenes guardadas exitosamente en formato WebP.")