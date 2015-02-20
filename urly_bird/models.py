from .app import db, bcrypt, login_manager
from flask.ext.login import UserMixin


class Urly_bird(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    short = db.Column(db.String(255), nullable=False, unique=True)

    long = db.Column(db.String(255), nullable=False, unique=True)

    def __repr__(self):
        return "<Urly-bird {}>".format(self.short)


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

    password = property(get_password, set_password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.encrypted_password, password)

    def __repr__(self):
        return "<User {}>".format(self.email)
