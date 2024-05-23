import os
from dotenv import load_dotenv
from google.cloud import vision
import google.generativeai as genai

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Configurar Google Generative AI
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
]

# Crear el modelo generativo
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    safety_settings=safety_settings,
    generation_config=generation_config,
)

def analyze_image(image_path):
    """Usa Google Cloud Vision API para analizar una imagen y devolver una descripción."""
    client = vision.ImageAnnotatorClient()

    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.label_detection(image=image)
    labels = response.label_annotations

    descriptions = [label.description for label in labels]
    return ', '.join(descriptions)

def describe_image(image_path):
    """Genera una descripción de la imagen usando Google Generative AI."""
    image_description = analyze_image(image_path)
    input_text = f"Dime qué ves en la foto: {image_description}"
    response = model.generate_content(input_text)
    print(response.text)
    return response


def prueba():
    input_text = "puedes recibir documentos de txt directos o los tengo que convertir a texto plano?"
    response = model.generate_content(input_text)
    print(response.text)
    return response

if __name__ == "__main__":
    # Ejecutar la prueba para generar contenido basado en una pregunta
    #prueba()
    
    # Ruta de la imagen
    img_path = "uploads\\perro.jpg"

    print("Ruta de la imagen:", img_path)
    describe_image(img_path)
