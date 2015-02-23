from . import db, bcrypt, login_manager
from flask.ext.login import UserMixin

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    encrypted_password = db.Column(db.String(60))

    def get_password(self):
        return getattr(self, "_password", None)

    def set_password(self, password):
        self._password = password
        self.encrypted_password = bcrypt.generate_password_hash(password)

    password = property(get_password, set_password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.encrypted_password, password)

    @property
    def user_links(self):
        return [links.url for link in self.links]

    def __repr__(self):
        return "<User {}>".format(self.email)


class Links(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    url = db.Column(db.String(255), unique=True)
    text = db.Column(db.String(255))
    short = db.Column(db.String(6), nullable=False, unique=True)
    user = db.relationship('User', backref=db.backref('links', lazy='dynamic'))


    def __repr__(self):
        return "URL {}".format(self.url)
