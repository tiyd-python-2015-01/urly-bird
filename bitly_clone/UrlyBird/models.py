from . import db, bcrypt, login_manager
from flask.ext.login import UserMixin
from datetime import datetime

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

    password = property(get_password, set_password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.encrypted_password, password)

    def __repr__(self):
        return "<User {}>".format(self.email)

class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(255), nullable= False)
    shortlink = db.Column(db.String(255), unique=True, nullable = False)
    title = db.Column(db.String(255), unique=True, nullable= False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    sub_date = db.Column(db.DateTime)
    click_count = db.Column(db.Integer)

    user = db.relationship('User')
