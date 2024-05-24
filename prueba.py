"""from PIL import Image
import os

img_path = "uploads/003.jpg"

# Verificar si la ruta es válida
if os.path.exists(img_path):
    print(f"La imagen existe en la ruta: {img_path}")
    # Cargar y mostrar la imagen
    img = Image.open(img_path)
    img.show()
else:
    print(f"La imagen no se encuentra en la ruta: {img_path}")

"""
# pip install Pillow

import google.generativeai as genai
from PIL import Image
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel(model_name="gemini-pro-vision")

# Abre una imagen desde un archivo
imagen = Image.open("uploads\perro.jpg")
imagen.show()

response = model.generate_content(["Dime que ves y ya", imagen])
print(response.text)