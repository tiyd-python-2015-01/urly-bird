from flask_wtf import Form
from wtforms.fields.html5 import URLField
from wtforms.validators import DataRequired, url, Email, EqualTo


class UrlForm(Form):
    text = URLField('text', validators=[DataRequired(), url()])


class Login(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])


class RegisterUser(Form):
    name = SringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired(),
                             EqualTo('password_verification',
                             message="Passwords must match")])
    password_verify = PasswordField('Repeat Password',
                                    validators=[DataRequired()])
