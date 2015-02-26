from . import db, bcrypt, login_manager
from flask.ext.login import UserMixin
from sqlalchemy import func, and_
from datetime import date, timedelta, datetime

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

    def link_clicks(self):
        return len(Click.query.filter_by(link_id=self.id).all())

    clicks = property(link_clicks)

    @property
    def clicks_last_30(self):
        return len(self.clicks_per_day())

    def clicks_per_day(self, days=30):
        days = timedelta(days=days)
        date_from = date.today() - days


        click_date = func.cast(Click.timestamp, db.Date)
        return db.session.query(click_date, func.count(Click.id)). \
            group_by(click_date). \
            filter(and_(Click.link_id == self.id,
                        click_date >= str(date_from))). \
            order_by(click_date).all()


    def to_dict(self):
        return {'id': self.id,
                'url': self.url,
                'text': self.text,
                'short': self.short}

    def __repr__(self):
        return "URL {}".format(self.url)


class Click(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    link_id = db.Column(db.Integer, db.ForeignKey('links.id'))
    timestamp = db.Column(db.DateTime)
    ip = db.Column(db.String(255))
    user_agent = db.Column(db.String(255))

    link = db.relationship("Links", backref='linkclicks')

    def __repr__(self):
        return "Clicks to Date: {}".format(self.count)
