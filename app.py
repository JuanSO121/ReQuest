from flask import Flask
from blueprints.index.index import index_bp
from blueprints.front.home import home_bp  # Importa home_bp en lugar de app
from extensions import configure_extensions

app = Flask(__name__)

# Seguridad de información
app.config['SECRET_KEY'] = 'your_secret_key'
# Carpetas Imagenes
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads/imagenes'
# Carpetas Documentos
app.config['UPLOADED_DOCUMENTS_DEST'] = 'uploads/pdf'

app.config['UPLOADED_WORD_DEST'] = 'uploads/word'

app.config['GENERATED_UPLOADS_FOLDER'] = 'uploads/generated'

# Imágenes Confi
configure_extensions(app)

# Blueprints modularizar código
app.register_blueprint(index_bp)
app.register_blueprint(home_bp)  # Registra el blueprint home_bp

if __name__ =='__main__':   
    app.run(debug=True)
