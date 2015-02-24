from . import db, bcrypt, login_manager
from flask.ext.login import UserMixin
from hashids import Hashids

hasher = Hashids()

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


class BookmarkedUrl(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    longurl = db.Column(db.String(255), nullable=False, unique=True)
    shorturl = db.Column(db.String(255), unique=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))

    def set_shorturl(self):
         self.shorturl = hasher.encode(self.id)

    def __repr__(self):
        return "<Url: {}>".format(self.longurl)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
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
        return"<User {}>".format(self.email)
