from flask import Blueprint, render_template, current_app, flash, send_file, request, redirect, url_for, session
from form import MyFormDocument
from werkzeug.utils import secure_filename
import os
from io import BytesIO
from classe.document import DocumentExtractor
from classe.gemini import geminiApi

home_bp = Blueprint("home", __name__, template_folder="templates")

@home_bp.route('/')
def home():
    return render_template('home.html')

@home_bp.route('/clasificacion', methods=['GET', 'POST'])
def clasificacion():
    return render_template('clasificacion.html')

@home_bp.route('/priorizacion', methods=['GET', 'POST'])
def priorizacion():
    form = MyFormDocument()
    if form.validate_on_submit():
        description = form.description.data
        file = form.file.data
        if not description:
            flash('Por favor, proporcione una descripción.', 'error')
        elif not file:
            flash('Por favor, suba un documento.', 'error')
        else:
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOADED_DOCUMENTS_DEST'], filename)
            
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            file.save(file_path)
            
            extractor = DocumentExtractor()
            prioritized_requirements = extractor.extract_prioritized_requirements(file_path)
            
            if prioritized_requirements:
                flash('Requisitos priorizados obtenidos correctamente.', 'success')
                session['historias_usuario'] = prioritized_requirements  # Almacenar en sesión
                return render_template('priorizacion.html', form=form, historias_usuario=prioritized_requirements)
            else:
                flash('Error al procesar el documento.', 'error')

    return render_template('priorizacion.html', form=form)

@home_bp.route('/HU_imagen', methods=['GET', 'POST'])
def HU_imagen():
    form = MyFormDocument()
    if form.validate_on_submit():
        description = form.description.data
        file = form.file.data
        if not description:
            flash('Por favor, proporcione una descripción.', 'error')
        elif not file:
            flash('Por favor, suba una imagen.', 'error')
        else:
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], filename)
            
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            file.save(file_path)
            
            api = geminiApi()
            api.configure()
            historias_usuario = api.generate_user_story(file_path)
            
            session['historias_usuario'] = historias_usuario  # Almacenar en sesión
            
            return render_template('HU_imagen.html', form=form, historias_usuario=historias_usuario)
    
    return render_template('HU_imagen.html', form=form, historias_usuario=None)

@home_bp.route('/download_document/<format>', methods=['GET'])
def download_document(format):
    # Obtener las historias de usuario generadas desde la sesión
    historias_usuario = session.get('historias_usuario')
    if not historias_usuario:
        flash('No hay historias de usuario disponibles para descargar.', 'error')
        return redirect(url_for('home.home'))

    # Generar el documento en el formato especificado
    if format == 'word':
        document_content = generate_word_document(historias_usuario)
        filename = 'historias_usuario.docx'
        mimetype = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    elif format == 'pdf':
        document_content = generate_pdf_document(historias_usuario)
        filename = 'historias_usuario.pdf'
        mimetype = 'application/pdf'
    elif format == 'txt':
        document_content = generate_txt_document(historias_usuario)
        filename = 'historias_usuario.txt'
        mimetype = 'text/plain'
    else:
        return 'Formato no admitido', 400

    output_folder = current_app.config['GENERATED_UPLOADS_FOLDER']
    os.makedirs(output_folder, exist_ok=True)
    file_path = os.path.join(output_folder, filename)
    with open(file_path, 'wb') as f:
        f.write(document_content)

    return send_file(file_path, as_attachment=True, download_name=filename, mimetype=mimetype)

def generate_word_document(historias_usuario):
    from docx import Document
    document = Document()
    for historia in historias_usuario:
        document.add_paragraph(historia)
    byte_io = BytesIO()
    document.save(byte_io)
    byte_io.seek(0)  # Reset the stream position to the beginning
    return byte_io.getvalue()

def generate_pdf_document(historias_usuario):
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    byte_io = BytesIO()
    c = canvas.Canvas(byte_io, pagesize=letter)
    y = 750
    for historia in historias_usuario:
        c.drawString(40, y, historia)
        y -= 20
    c.showPage()
    c.save()
    byte_io.seek(0)  # Reset the stream position to the beginning
    return byte_io.getvalue()

def generate_txt_document(historias_usuario):
    content = "\n".join(historias_usuario)
    return content.encode('utf-8')