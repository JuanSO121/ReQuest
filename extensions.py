from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class

photos = UploadSet('photos', IMAGES)

def configure_extensions(app):
    configure_uploads(app, photos)
    patch_request_class(app, 16 * 1024 * 1024)  # Set maximum file size, default is 16MB