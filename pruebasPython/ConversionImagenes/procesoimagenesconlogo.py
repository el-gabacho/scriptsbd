import os
from PIL import Image

# Rutas de las carpetas
carpeta_imagenes = r'C:\Users\Anonymous\Desktop\7790'
logo_path = r'C:\Users\Anonymous\Desktop\LogoGabacho\logo.png'
output_folder = r'C:\Users\Anonymous\Desktop\IMGabachoLogo'

# Crear la carpeta de salida si no existe
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Cargar el logo
logo = Image.open(logo_path).convert("RGBA")  # Convertir a RGBA para permitir la transparencia

# Iterar sobre cada imagen en la carpeta 7790
for filename in os.listdir(carpeta_imagenes):
    if filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg'):
        # Cargar la imagen
        img_path = os.path.join(carpeta_imagenes, filename)
        img = Image.open(img_path).convert("RGBA")  # Convertir a RGBA también

        # Redimensionar el logo en función del tamaño de la imagen
        img_width, img_height = img.size
        factor_escala = 0.1  # Logo será el 10% del ancho de la imagen
        new_logo_width = int(img_width * factor_escala)
        new_logo_height = int(new_logo_width * (logo.height / logo.width))  # Mantener la proporción
        logo_resized = logo.resize((new_logo_width, new_logo_height), Image.LANCZOS)  # Usar LANCZOS

        # Pegar el logo en la posición (10, 10)
        img.paste(logo_resized, (10, 10), logo_resized)  # (10, 10) es la nueva posición

        # Guardar la nueva imagen en la carpeta IMGabachoLogo
        output_path = os.path.join(output_folder, filename)
        img = img.convert("RGB")  # Convertir de nuevo a RGB si lo necesitas en formatos como JPEG
        img.save(output_path)

        print(f'Imagen procesada: {filename}')

print('Proceso completado.')
