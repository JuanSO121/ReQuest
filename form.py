from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class MyForm(FlaskForm):
    text = StringField('Text', validators=[DataRequired()])
    image = FileField('Image', validators=[DataRequired()])
    submit = SubmitField('Submit')

class MyFormDocument(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    file = FileField('File', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'jpeg', 'png', 'pdf', 'doc', 'docx'], 'Only images, PDFs, or Word documents are allowed!')
    ])
    submit = SubmitField('Enviar')

class ImageUploadForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    file = FileField('File', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'jpeg', 'png', 'pdf', 'doc', 'docx'], 'Only images, PDFs, or Word documents are allowed!')
    ])
    submit = SubmitField('Enviar')