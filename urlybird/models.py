from . import db
from flask.ext.login import UserMixin


class BookmarkedUrl(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    longurl = db.Column(db.String(255), nullable=False, unique=True)
    shorturl = db.Column(db.String(255), nullable=False, unique=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    
    def __init__(self, text):
        self.url = text

    def __repr__(self):
        return "<Url: {}>".format(self.url)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    encrypted_password = db.Column(db.String(60))

    def __repr__(self):
        return"<User {}>".format(self.email)
