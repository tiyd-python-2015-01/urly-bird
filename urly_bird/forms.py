from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.fields.html5 import EmailField, URLField
from wtforms.validators import DataRequired, Email, EqualTo, URL

class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class RegistrationForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField(
        'Password',
        validators=[DataRequired(),
                    EqualTo('password_verification',
                            message="Passwords must match")])
    password_verification = PasswordField('Repeat password')

class URLForm(Form):
    url =  URLField('URL', validators=[DataRequired(), URL()])
    description = StringField('description')

class editURL(Form):
    original_link =  URLField('original_link', validators=[DataRequired(), URL()])
    description = StringField('description')