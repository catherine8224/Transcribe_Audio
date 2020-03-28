from flask_wtf import Form, validators, FlaskForm
from wtforms import StringField, TextField, BooleanField, IntegerField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, length, ValidationError
from flask_wtf.file import FileField, FileAllowed, FileRequired


class ContactForm(Form):
  firstname = StringField("First Name", validators=[DataRequired()])
  lastname = StringField("Last Name", validators=[DataRequired()])
  email = StringField("Email",  validators=[DataRequired(), Email()])
  subject = StringField("Subject", validators=[DataRequired()])
  message = TextAreaField("Message", validators=[DataRequired()])
  audiofile = FileField('Audio File', validators=[FileRequired(), FileAllowed(['wav', 'mp3'], 'Audio Files only!')])
  submit = SubmitField("Send")
