from flask import Blueprint, render_template, current_app
from blueprints.index.index import index_bp
from extensions import configure_extensions

home_bp = Blueprint("home", __name__, template_folder="templates")

@home_bp.route('/')
def home():
    return render_template('home.html')

@home_bp.route('/HU_imagen', methods=['GET', 'POST'])
def HU_imagen():
    return render_template('HU_imagen.html')

@home_bp.route('/clasificacion', methods=['GET', 'POST'])
def clasificacion():
    return render_template('clasificacion.html')

@home_bp.route('/priorizacion', methods=['GET', 'POST'])
def priorizacion():
    return render_template('priorizacion.html')