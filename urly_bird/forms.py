from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, EqualTo


class LoginForm(Form):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])


class RegistrationForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password',
        validators=[DataRequired(),
                    EqualTo('password_verification',
                            message="Passwords must match.")])
    password_verification = PasswordField('Repeat Password')


class LinkForm(Form):
    link = StringField('Enter Link:', validators=[DataRequired()])
