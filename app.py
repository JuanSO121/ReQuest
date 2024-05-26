from flask import Flask
from blueprints.index.index import index_bp
from extensions import configure_extensions

app = Flask(__name__)

#Seguridad de información
app.config['SECRET_KEY'] = 'your_secret_key'
#Carpetas Imagenes
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads/imagenes'
#Carpeta PDF
app.config['UPLOADED_DOCUMENTS_DEST'] = 'uploads/pdf'


configure_extensions(app)
#Blueprints modularizar codigo
app.register_blueprint(index_bp)

if __name__ =='__main__':   
    app.run(debug=True)