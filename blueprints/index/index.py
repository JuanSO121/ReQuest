from flask import Blueprint, render_template, redirect, request, current_app
from form import MyFormDocument
from werkzeug.utils import secure_filename
from extensions import photos, documents  # Import photos and documents
import os
from classe.gemini import geminiApi
from classe.document import DocumentExtractor

index_bp = Blueprint("index", __name__, template_folder="templates")

@index_bp.route("/", methods=['GET', 'POST'])
def document(): 
    form = MyFormDocument()

    if form.validate_on_submit():
        # Obtiene datos del formulario
        text = form.text.data
        file = form.document.data
        filename = secure_filename(file.filename)
        file_extension = filename.rsplit('.', 1)[1].lower()

        # Obtener el nombre base del archivo
        base_name = filename.rsplit('.', 1)[0]

        # Nueva extensión que deseas usar
        new_extension = "pdf"

        # Crear el nuevo nombre agregando la palabra "converted" y la nueva extensión
        new_filename = f"{base_name}_converted.{new_extension}"
        
        if file_extension in ['jpg', 'jpeg', 'png']:
            # Guarda la imagen
            image_path = os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], filename)
            file.save(image_path)
            
            # Genera historia de usuario
            api = geminiApi()
            api.configure()
            user_story = api.generate_user_story(image_path)
            
            return f'Texto: {text}. Filename: {filename}. Historia de usuario: {user_story}'
        
        elif file_extension in ['docx']:
            

            document_path = os.path.join(current_app.config['UPLOADED_WORD_DEST'], filename)

            pdf_path = os.path.join(current_app.config['UPLOADED_DOCUMENTS_DEST'], new_filename)

            file.save(document_path)
            file.save(pdf_path)
            
            extract = process_extension(file_extension, document_path,pdf_path)
            extract.geminiApi.configure_2()
            text = extract.geminiApi.generate_user_story_info(extract.geminiApi.text_document)
            print(text)
            
            return f'Texto: {text}. Filename: {filename}. La extensión del documento es: {file_extension}'
        else:
            return f'Extensión no soportada: {file_extension}'
    else:
        return render_template('document.html', form=form)

@index_bp.route("/hello")
def hello():
    return "Hello world again!"

@index_bp.route("/hello/<name>")
def hello_name(name):
    return f"Hello {name}!"






def process_extension(extension, document_path, pdf_path):
    if extension == 'pdf':
        extract = DocumentExtractor()
        extract.extract_text_from_pdf(document_path)
        #print(extract.geminiApi.text)
        return extract
    elif extension in ['doc', 'docx']:
        extract = DocumentExtractor()
        extract.convert_word_to_pdf(document_path,pdf_path)
        extract.extract_text_from_pdf(pdf_path)
        #print(extract.geminiApi.text)
        return extract
    elif extension == 'txt':
        print('Se detectó un archivo de texto. Procesando...')
        return None
    else:
        print('No se reconoce la extensión del archivo.')
