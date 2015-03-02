from . import db, bcrypt, login_manager
from flask.ext.login import UserMixin
from hashids import Hashids
from sqlalchemy import func

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


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    original_link = db.Column(db.text, nullable=False)
    short_link = db.Column(db.text)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    description = db.Column(db.Text)
    date = db.Column(db.DateTime)
    clicks = db.relationship('Click', backref='link', lazy='select')

    def shorten_url(self):
        self.short_link = Hashids()
        return self.short_link

    @property
    def clicks_by_day(self):
        click_date = func.cast(Click.date, db.Date)
        return db.session.query(func.count(Click.id), click_date).group_by(click_date).order_by(click_date).all()

    def to_dict(self):
        return {'id': self.id,
                'date': self.date,
                'original_link': self.original_link,
                'short_link': self.short_link,
                'description': self.description}


class Click(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    link_id = db.Column(db.Integer, db.ForeignKey('link.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    ip = db.Column(db.String(20))
    date = db.Column(db.DateTime)


from . import views