from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.fields.html5 import EmailField, URLField
from wtforms.validators import DataRequired, Email, EqualTo, URL


class LoginForm(Form):
    name = StringField('User Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class RegisterForm(Form):
    name = StringField('User Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField(
        'Password',
        validators=[DataRequired(),
                    EqualTo('password_verification',
                            message='Passwords must match')])
    password_verification = PasswordField('Repeat password')


class CreateLinkForm(Form):
    long_link = URLField("Original Link", validators=[DataRequired(), URL()])


class LinkNotesForm(Form):
    notes = StringField("Link Notes", validators=[DataRequired()])


class CustomLinkForm(Form):
    custom_link = StringField("Custom Link", validators=[DataRequired()])