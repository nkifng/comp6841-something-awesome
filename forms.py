from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class EncryptionForm(FlaskForm):
    key = StringField("Enter Secret Key", validators=[DataRequired()])
    file = FileField("Upload File", validators=[DataRequired()])
    submit = SubmitField('Encrypt')

class DecryptionForm(FlaskForm):
    decrypt_key = StringField("Enter Secret Key", validators=[DataRequired()])
    file = FileField("Upload File", validators=[DataRequired()])
    submit = SubmitField('Decrypt')

class StegEncForm(FlaskForm):
    message = StringField("Enter Secret Message", validators=[DataRequired()])
    file = FileField("Upload Image", validators=[DataRequired()])
    submit = SubmitField('Encrypt')

class StegDecForm(FlaskForm):
    file = FileField("Upload Image", validators=[DataRequired()])
    submit = SubmitField('Decrypt')

class ChaosEncForm(FlaskForm):
    file = FileField("Upload Image", validators=[DataRequired()])
    submit = SubmitField('Encrypt')