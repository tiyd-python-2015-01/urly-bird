from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, URL
from wtforms.fields.html5 import EmailField

class LoginForm(Form):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])


class RegistrationForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),
                              EqualTo('verify_password',
                                       message='Passwords did not match')])
    verify_password = PasswordField('Verify Password')


class AddLink(Form):
    url = StringField('URL', validators=[URL()])
    text = StringField('Short Description')

class EditLink(Form):
    url = StringField('URL', validators=[URL()])
    text = StringField('Short Description')
