from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SubmitField

class upload_edf_form(FlaskForm):
    edf_file = FileField('EDF File', name='edf_file',validators=[FileAllowed(['edf'], 'Only .edf files are allowed')])
    submit = SubmitField('Upload File')