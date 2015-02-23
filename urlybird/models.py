from .app import db
from .extensions import bcrypt, login_manager
from flask.ext.login import UserMixin


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False, unique=False)
    url = db.Column(db.String(255), nullable=False, unique=True)
    short_url = db.Column(db.String(10), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=True, unique=False)

    def __repr__(self):
        return "<URL {}>".format(self.url)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    encrypted_password = db.Column(db.String(60))

    def get_password(self):
        return getattr(self, "_password", None)
        return self._password

    def set_password(self, password):
        self._password = password
        self.encrypted_password = bcrypt.generate_password_hash(password)

    password = property(get_password, set_password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.encrypted_password, password)

    def __repr__(self):
        return "<User {}>".format(self.email)

class BookmarkUser(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('bookmark.id'))

    bookmark = db.relationship('Bookmark',
                               backref=db.backref('BookmarkUser',
                               lazy='dynamic'))
    user = db.relationship('User')

    def get_clicks(self):
        return len(Click.query.filter_by(item_id=self.item_id).all())

    clicks = property(get_clicks)

    def __repr__(self):
        return "<User {} | Item {}>".format(self.user_id, self.item_id)

class Click(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_id = db.Column(db.Integer, db.ForeignKey('bookmark.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime)

    def __repr__(self):
        return "<Item {} | User {} | Time {}>".format(self.item_id,
                                                      self.user_id,
                                                      self.timestamp)
