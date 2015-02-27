from . import db, bcrypt, login_manager
from flask.ext.login import UserMixin



@login_manager.user_loader
def load_user(id):
    return User.query.get(id)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    encrypted_password = db.Column(db.String(60))
    links = db.relationship('Links', backref='user',
                                lazy='dynamic')

    def get_password(self):
        return getattr(self, "_password", None)
        return self._password

    def set_password(self, password):
        self._password = password
        self.encrypted_password = bcrypt.generate_password_hash(password)

    password = property(None, set_password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.encrypted_password, password)

    @property
    def all_links(self):
        return [links.url for links in self.links]

    def __repr__(self):
        return "<User {}>".format(self.email)

class Links(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(255), unique=True, nullable=False)
    shortlink = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.String(255), unique=False, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #add new column for...run a query matching how many times the links
    #have been of the link ID's match the link_id from Clicks model

    def __repr__(self):
        return "<Links {}>".format(self.email)


class Clicks(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    link_id = db.Column(db.Integer, db.ForeignKey('links.id'))
    datetime = db.Column(db.DateTime)

    def __repr__(self):
        return "<Links {}>".format(self.email)

# Clinton's freeshelf example from Friday
# class Favorite(db.Model):
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
#     user = db.relationship('User', backref=db.backref('favorites', lazy='dynamic'))
#     book = db.relationship('Book')
