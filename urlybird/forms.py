from flask_wtf import Form

class UrlForm(Form):
    text = StringField('text', validators=[DataRequired()])
