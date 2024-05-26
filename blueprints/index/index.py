from flask import Blueprint, render_template, redirect, request
from form import MyForm
from extensions import photos  # Import photos
import os
from classe.gemini import geminiApi


index_bp = Blueprint("index", __name__, template_folder="templates")

@index_bp.route("/")
def index():
    return render_template('index.html')

@index_bp.route("/hello")
def hello():
    return "Hello world again!"

@index_bp.route("/hello/<name>")
def hello_name(name):
    return f"Hello {name}!"


@index_bp.route("/HU", methods=['GET', 'POST'])
def getanswerd():
  from app import app
  form = MyForm()
  if form.validate_on_submit():
    filename = photos.save(form.image.data)
    print("Nombre del archivo guardado:", filename)

    text = form.text.data
    image_path = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], filename)
    print("path",image_path)

    api = geminiApi()  
    historias_usuario = api.generate_user_story(image_path)

    return f"Texto: {text}.User Stories: {historias_usuario}"
  return render_template('upload.html', form=form)


