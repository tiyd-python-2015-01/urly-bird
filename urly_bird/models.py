from .app import db, bcrypt, login_manager
from flask.ext.login import UserMixin

"""Add your models here."""

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

    def __str__(self):
        return self.email

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))


class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    long_address = db.Column(db.String(255))
    short_address = db.Column(db.String(255))
    owner = db.Column(db.Integer)  #User ID of the owner
    clicks = db.Column(db.Integer) #Number of Clicks for Link Tracking
