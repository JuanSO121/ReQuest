from flask_uploads import UploadSet, configure_uploads, patch_request_class, IMAGES

photos = UploadSet('photos', IMAGES)
documents = UploadSet('documents', ('pdf', 'doc', 'docx'))

def configure_extensions(app):
    configure_uploads(app, photos)
    configure_uploads(app, documents)
    patch_request_class(app, 16 * 1024 * 1024)  # Establecer el tamaño máximo de archivo
