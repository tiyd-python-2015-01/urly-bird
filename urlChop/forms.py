from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, EqualTo, URL


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    #submit = SubmitField('Submit')#this is a flask-bootstrap thing


class RegistrationForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField(
        'Password',
        validators=[DataRequired(),
                    EqualTo('password_verification',
                            message="Passwords must match")])
    password_verification = PasswordField('Repeat password')
    #submit = SubmitField('Submit')#this is a flask-bootstrap thing


class Newlink(Form):
   description = StringField("Description", validators=[DataRequired()])
   url = StringField("Web Address", validators=[DataRequired(), URL()])
   # submit = SubmitField('Submit')#this is a flask-bootstrap thing
   # name = StringField('Title', validators=[DataRequired()])
