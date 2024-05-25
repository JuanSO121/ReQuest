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

class geminiApi:
    def __init__(self,api_key):
        self.api_key=api_key
        self.model = self.configure()

    def configure(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        return genai.GenerativeModel(model_name="gemini-pro-vision")
    
    def generate_user_story(self, image_path):
        imagen = Image.open(image_path)
        prompt = f"dame las historias de usuario de este producto en formato de como, quiero, para"
        response = self.model.generate_content([prompt, imagen])
        return response.text
