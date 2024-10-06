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

# Iterar sobre cada imagen en la carpeta 7790
for filename in os.listdir(carpeta_imagenes):
    if filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.webp'):
        # Cargar la imagen
        img_path = os.path.join(carpeta_imagenes, filename)
        img = Image.open(img_path).convert("RGBA")  # Convertir a RGBA también

        # Crear una capa para la marca de agua
        watermark_layer = Image.new("RGBA", img.size)
        draw = ImageDraw.Draw(watermark_layer)

        # Definir la fuente y tamaño
        font_size = int(img.size[1] / 10)  # 10% del alto de la imagen
        font = ImageFont.truetype(font_path, font_size)  # Usar la fuente personalizada

        # Calcular el tamaño del texto usando textbbox
        text_bbox = draw.textbbox((0, 0), watermark_text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        # Posicionar el texto en el centro
        position = ((img.size[0] - text_width) // 2, (img.size[1] - text_height) // 2)

        # Establecer el color con más opacidad (90% de opacidad = 230 en 255)
        opacity = int(255 * 0.90)  # 90% de opacidad
        fill_color = (232, 232, 232, opacity)  # Color gris claro con 90% de opacidad

        # Dibujar el texto en la capa de marca de agua con opacidad
        draw.text(position, watermark_text, fill=fill_color, font=font)  # Color con opacidad

        # Combinar la imagen original con la capa de marca de agua
        combined = Image.alpha_composite(img, watermark_layer)

        # Guardar la nueva imagen en formato WebP con compresión sin pérdida
        output_filename = os.path.splitext(filename)[0] + ".webp"  # Cambiar extensión a .webp
        output_path = os.path.join(output_folder, output_filename)
        combined.save(output_path, "WEBP", lossless=True)  # Guardar como WebP con compresión sin pérdida

        print(f'Imagen procesada: {filename}')

print('Proceso completado.')