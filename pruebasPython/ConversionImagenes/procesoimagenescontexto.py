import os
from PIL import Image, ImageDraw, ImageFont

# Rutas de las carpetas
carpeta_imagenes = r'C:\Users\Anonymous\Desktop\7790'
output_folder = r'C:\Users\Anonymous\Desktop\IMGabachoTexto'

# Crear la carpeta de salida si no existe
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Texto de marca de agua
watermark_text = "EL GABACHO"

# Cargar la fuente
font_path = r"C:\Users\Anonymous\Desktop\BonaNova-Bold.ttf"

# Inicializar un contador para el renombramiento
contador = {}

# Iterar sobre cada imagen en la carpeta de entrada
for filename in os.listdir(carpeta_imagenes):
    # Filtrar solo imágenes con extensiones válidas
    if filename.endswith(('.png', '.jpg', '.jpeg', '.webp')):
        # Extraer el nombre verdadero del archivo (antes de "-" o "_")
        base_name = filename.split('.')[0]  # Solo el nombre sin la extensión
        true_name = base_name.split('-')[0].split('_')[0]  # Obtener el nombre verdadero

        # Incrementar el contador para este nombre verdadero
        if true_name not in contador:
            contador[true_name] = 1
        else:
            contador[true_name] += 1

        # Cargar la imagen
        img_path = os.path.join(carpeta_imagenes, filename)
        img = Image.open(img_path).convert("RGBA")

        # Crear una capa para la marca de agua
        watermark_layer = Image.new("RGBA", img.size)
        draw = ImageDraw.Draw(watermark_layer)

        # Definir la fuente y tamaño
        font_size = int(img.size[1] / 10)  # 10% del alto de la imagen
        font = ImageFont.truetype(font_path, font_size)

        # Calcular el tamaño del texto usando textbbox
        text_bbox = draw.textbbox((0, 0), watermark_text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        # Posicionar el texto en el centro
        position = ((img.size[0] - text_width) // 2, (img.size[1] - text_height) // 2)

        # Establecer el color con 90% de opacidad
        opacity = int(255 * 0.90)
        fill_color = (232, 232, 232, opacity)

        # Dibujar el texto en la capa de marca de agua
        draw.text(position, watermark_text, fill=fill_color, font=font)

        # Combinar la imagen original con la capa de marca de agua
        combined = Image.alpha_composite(img, watermark_layer)

        # Generar el nuevo nombre de archivo
        new_filename = f"{true_name}_{contador[true_name]}.webp"  # Aquí se renombra correctamente
        output_path = os.path.join(output_folder, new_filename)
        combined.save(output_path, "WEBP", lossless=True)

        print(f'Imagen procesada y renombrada: {filename} -> {new_filename}')

print('Proceso completado.')
