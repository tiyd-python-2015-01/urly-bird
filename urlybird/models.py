from . import db

class LongUrl(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(255), nullable=False, unique=True)

    def __init__(self, text):
        self.url = text
        
    def __repr__(self):
        return "<Url: {}>".format(self.url)
