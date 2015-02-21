from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired


class UrlForm(Form):
    text = StringField('text', validators=[DataRequired()])
