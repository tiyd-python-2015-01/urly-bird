from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, EqualTo
from .models import User


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])


class RegistrationForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),
                             EqualTo('password_verification',
                             message="Passwords must match")])
    password_verification = PasswordField('Repeat password')


class LinkShortener(Form):
    link_name = StringField('Link Name', validators=[DataRequired()])
    url = StringField('URL', validators=[DataRequired()])
