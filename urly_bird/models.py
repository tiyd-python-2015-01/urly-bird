from . import db, bcrypt, login_manager
from flask.ext.login import UserMixin
from hashids import Hashids
from flask import redirect
from . import app


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    encrypted_password = db.Column(db.String(60))
    links = db.relationship('Link', backref='user', lazy='dynamic')
    clicks = db.relationship('Click', backref='user', lazy='dynamic')


    def get_password(self):
        return getattr(self, "_password", None)

    def set_password(self, password):
        self._password = password
        self.encrypted_password = bcrypt.generate_password_hash(password)

    password = property(get_password, set_password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.encrypted_password, password)

    def __repr__(self):
        return "<User {}>".format(self.email)

class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime)
    original_link = db.Column(db.String(255), nullable=False)
    short_link = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    description = db.Column(db.Text)
    clicks = db.relationship('Click', backref='link', lazy='dynamic')

    def get_short_link(self):
       salt = Hashids(salt="and pepper", min_length=1)
       hash = salt.encode(self.id)
       self.hash = hash
       self.short_link = hash

class Click(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    link_id = db.Column(db.Integer, db.ForeignKey('link.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.DateTime)



