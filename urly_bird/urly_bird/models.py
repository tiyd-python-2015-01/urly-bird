from . import db, bcrypt, login_manager, hashid
from flask.ext.login import UserMixin
from datetime import datetime
import random

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    encrypted_password = db.Column(db.String(60))

    def get_password(self):
        return getattr(self, "_password", None)

    def set_password(self, password):
        self._password = password
        self.encrypted_password = bcrypt.generate_password_hash(password)

    password = property(None, set_password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.encrypted_password, password)

    @property
    def links(self):
        return [link.shortlink for link in self.link]

    def __repr__(self):
        return "<User {}>".format(self.email)


class Link(db.Model):
    """user added urls"""
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(255), nullable=False)
    shortlink = db.Column(db.String(255), unique=True, nullable=False)
    title = db.Column(db.String(255), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.DateTime())
    links = db.relationship('User',
                            backref=db.backref('submitted', lazy='dynamic'))
    def set_short_link(self):
        self.short_link = hashid.encode(datetime.now().microsecond, random.randint(0, 100000))

    def __repr__(self):
        return url_for('index')+"{}".format(self.short_link)