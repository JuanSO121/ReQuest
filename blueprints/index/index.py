from flask import Blueprint, render_template, redirect, request
from form import MyForm
from extensions import photos  # Import photos

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
    form = MyForm()
    if form.validate_on_submit():
        filename = photos.save(form.image.data)
        text = form.text.data
        
        return f"Text: {text}, Image: {filename} uploaded successfully"
    return render_template('upload.html', form=form)
