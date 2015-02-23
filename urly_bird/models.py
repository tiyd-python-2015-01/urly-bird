from . import db, bcrypt, login_manager
from flask.ext.login import UserMixin


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    encrypted_password = db.Column(db.String(60))

    def set_password(self, password):
        self.encrypted_password = bcrypt.generate_password_hash(password)

    password = property(None, set_password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.encrypted_password, password)

    def __repr__(self):
        return "<User {}>".format(self.email)

    @property
    def links(self):
        user_links = [link for link in self.submitted]
        user_links.reverse()
        return user_links


class Link(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    short = db.Column(db.String(10))
    original = db.Column(db.String(255), nullable=False)
    owner = db.Column(db.Integer, db.ForeignKey(User.id))
    title = db.Column(db.String(60))
    description = db.Column(db.String(255))
    date = db.Column(db.DateTime())
    links = db.relationship('User',
                            backref=db.backref('submitted', lazy='dynamic'))
    @property
    def clicks(self):
        return [click for click in self.clicks]


class Click(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.Integer, db.ForeignKey(Link.id))
    date = db.Column(db.DateTime())
    user = db.Column(db.String(60))
    clicks = db.relationship('Link', backref=db.backref('clicked', lazy='dynamic'))
