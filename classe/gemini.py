import google.generativeai as genai
from PIL import Image
import os

class geminiApi:
    def __init__(self):
        self.api_key=os.getenv("GEMINI_API_KEY")
        self.model = self.configure()
        self.text = None

    def configure(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        return genai.GenerativeModel(model_name="gemini-pro-vision")
    
    def text_document(self, text):
        self.text = text
    
    def generate_user_story(self, image_path):
        imagen = Image.open(image_path)
        prompt = f"dame solo una historia de usuario con el formato de como, quiero, para"
        response = self.model.generate_content([prompt, imagen])
        return response.text

    
