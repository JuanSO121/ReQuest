from flask import Blueprint, render_template, redirect, request, current_app
from form import MyForm, MyFormDocument
from werkzeug.utils import secure_filename
from extensions import photos, documents  # Import photos
import os
from classe.gemini import geminiApi
from classe.document import DocumentExtractor

index_bp = Blueprint("index", __name__, template_folder="templates")

@index_bp.route("/index", methods=['GET', 'POST'])
def document():
    form = MyFormDocument()

    if form.validate_on_submit():
        # Obtiene los datos del formulario
        text = form.text.data
        document = form.document.data
        document_extension = document.filename.rsplit('.', 1)[1].lower()
            
        # Guarda el documento en el servidor
        filename = secure_filename(document.filename)
        document_path = os.path.join(current_app.config['UPLOADED_DOCUMENTS_DEST'], filename)
        document.save(document_path)
        process_extension(document_extension,document_path)

        # Devuelve una respuesta al usuario con la información del documento
        return f'La extensión del documento es: {document_extension}, y el texto es: {text}'
    else:
        return render_template('document.html', form=form)



@index_bp.route("/hello")
def hello():
    return "Hello world again!"

@index_bp.route("/hello/<name>")
def hello_name(name):
    return f"Hello {name}!"

@index_bp.route("/HU", methods=['GET', 'POST'])
def getanswerd():
    form = MyForm()
    if form.validate_on_submit():
        filename = photos.save(form.image.data)
        print("Nombre del archivo guardado:", filename)
        text = form.text.data
        
        # Obtener el path de la imagen subida usando current_app
        image_path = os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], filename)
        print("Path de la imagen:", image_path)

        # Aquí podrías usar tu API para procesar la imagen
        api = geminiApi()  
        historias_usuario = api.generate_user_story(image_path)

        return f"Texto: {text}. Historia de usuario: {historias_usuario}"
    return render_template('upload.html', form=form)

    
    
    
"FUNCIÓN APARTE "
def process_extension(extension,document_path):
    if extension == 'pdf':
        extract = DocumentExtractor()
        extract.extract_text_from_pdf(document_path)
        print(extract.geminiApi.text)
    elif extension == 'doc' or extension == 'docx':
        return 'Se detectó un documento de Word. Procesando...'
    elif extension == 'txt':
        return 'Se detectó un archivo de texto. Procesando...'
    else:
        return 'No se reconoce la extensión del archivo.'
