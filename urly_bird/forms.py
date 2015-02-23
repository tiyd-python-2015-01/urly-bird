from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.fields.html5 import EmailField, URLField
from wtforms.validators import DataRequired, Email, EqualTo



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


class LinkAddForm(Form):
    long = URLField('Long', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    description = StringField('Description')

class LinkUpdateForm(Form):
    long = URLField('Long', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    description = StringField('Description')
