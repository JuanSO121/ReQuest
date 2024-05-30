import google.generativeai as genai
from PIL import Image
import os
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO


class geminiApi:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = None
        self.text_document = None

    def configure(self):
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name="gemini-pro-vision")
        return self.model

    def configure_2(self):
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name="gemini-pro")
        return self.model
    
    def generate_user_story(self, image_path):
        imagen = Image.open(image_path)
        prompt = "dame dos historias de usuario con el formato de como, quiero, para"
        response = self.model.generate_content([prompt, imagen])
        historias_usuario = response.text.split('\n')  
        return [historia.strip() for historia in historias_usuario if historia.strip()]
    
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
        estructura = 'Prioriza los siguientes requisitos según su importancia, enumerándolos del más importante al menos importante:'
        full_prompt = f'{estructura} {text_R}'
        response = self.model.generate_content(full_prompt)
        prioritization = response.text
        print("Priorización de requisitos generada:")
        print(prioritization)

        # Parsear la respuesta para obtener la lista de requisitos priorizados
        prioritized_requirements = [req.strip() for req in prioritization.split('\n') if req.strip()]

        return prioritized_requirements






def generate_word_document(historias_usuario):
    doc = Document()
    doc.add_heading('Historias de Usuario', 0)
    for historia in historias_usuario:
        doc.add_paragraph(historia)
    byte_io = BytesIO()
    doc.save(byte_io)
    byte_io.seek(0)
    return byte_io.getvalue()

def generate_pdf_document(historias_usuario):
    byte_io = BytesIO()
    c = canvas.Canvas(byte_io, pagesize=letter)
    width, height = letter
    c.drawString(100, height - 40, "Historias de Usuario")
    y = height - 60
    for historia in historias_usuario:
        c.drawString(100, y, historia)
        y -= 20
        if y < 40:
            c.showPage()
            y = height - 40
    c.save()
    byte_io.seek(0)
    return byte_io.getvalue()

def generate_txt_document(historias_usuario):
    content = "\n".join(historias_usuario)
    return content.encode('utf-8')