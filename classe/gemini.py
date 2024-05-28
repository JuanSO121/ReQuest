import google.generativeai as genai
from PIL import Image
import os

class geminiApi:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = None
        self.text = None

    def configure(self):
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name="gemini-pro-vision")
        return self.model

    def configure_2(self):
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name="gemini-pro")
        return self.model
    
    def text_document(self, text):
        self.text = text
    
    def generate_user_story(self, image_path):
        imagen = Image.open(image_path)
        prompt = f"dame solo una historia de usuario con el formato de como, quiero, para"
        response = self.model.generate_content([prompt, imagen])
        return response.text

    def generate_user_story_info(self, info_document):
        prompt = info_document
        estructura = 'dame solo una historia de usuario con el formato de como, quiero, para'
        full_prompt = f'{estructura} {prompt}'
        response = self.model.generate_content(full_prompt)
        return response.text


#Metodos de obtención de información mediante texto con respecto a otras funcionalidades 
    def generate_requirements_functionality(self, info):
        prompt = info
        estructura = 'Con esta estructura quiero 5 requisitos funcionales: [Sujeto]-[Acción]-[Valor]. Con respecto a estas Historias de usuario: '
        full_prompt = f'{estructura} {prompt}'
        response = self.model.generate_content(full_prompt)
        return response.text
    
    def generate_requirements_functionality(self, info):
        prompt = info
        estructura = 'Con esta estructura quiero 5 Requerimientos No funcionales : [Condición]-[Sujeto]-[Acción]-[Objeto]-[Restricción]. Con respecto a estas Historias de usuario: '
        full_prompt = f'{estructura} {prompt}'
        response = self.model.generate_content(full_prompt)
        return response.text

    def generate_classification_prioritization(self, text_R):
        prompt = text_R
        estructura = 'Quiero que priorices esta información a la que tenga mayor demanda hasta la que tenga menor demanda enumerandolos'
        full_prompt = f'{estructura} {prompt}'
        response = self.model.generate_content(full_prompt)
        return response.text
