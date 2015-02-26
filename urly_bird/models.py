from . import db, bcrypt, login_manager
from datetime import date, timedelta, datetime
from sqlalchemy import func, and_
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

    def clicks_by_day(self, days=30):
        days = timedelta(days=days)
        date_from = datetime.today() - days
        click_date = func.date_trunc('day', Click.date)

        return db.session.query(click_date, func.count(Click.id)). \
                                group_by(click_date). \
                                filter(and_(Click.link == self.id,
                                click_date >= str(date_from))). \
                                order_by(click_date).all()


class Click(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.Integer, db.ForeignKey(Link.id))
    date = db.Column(db.DateTime())
    user = db.Column(db.Integer)
    ip = db.Column(db.String(15))
    user_agent = db.Column(db.Text())
    clicks = db.relationship('Link',
                             backref=db.backref('clicked', lazy='dynamic'))
