from . import db, bcrypt, login_manager, hashid
import random
from flask import url_for
from flask.ext.login import UserMixin
from datetime import datetime
from sqlalchemy import func


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    long_link = db.Column(db.String(255), nullable=False)
    short_link = db.Column(db.String(255), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    description = db.Column(db.String(255))
    custom_links = db.relationship('Custom', backref='link', lazy='dynamic')
    clicks = db.relationship('Click', backref='link', lazy='dynamic')


    def set_short_link(self):
        self.short_link = hashid.encode(datetime.now().microsecond, random.randint(0, 100000))

    def __repr__(self):
        return "{}".format(self.short_link)

    def clicks_by_day(self):
        click_date = func.cast(Click.time_clicked, db.Date)
        return db.session.query(click_date, func.count(Click.id)). \
            group_by(click_date).filter_by(link_id=self.id). \
            order_by(click_date).all()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False)
    encrypted_password = db.Column(db.String(60))
    links = db.relationship('Link', backref='user', lazy='dynamic')
    links_clicks = db.relationship('Click', backref='user', lazy='dynamic')
    clicks = db.relationship('Click', backref='clicker', lazy='dynamic')


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

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password


class Custom(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start_link = db.Column(db.String(255), db.ForeignKey('link.short_link'))
    new_link = db.Column(db.String(255), unique=True)

    def __repr__(self):
        return self.new_link


class Click(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip_address = db.Column(db.String(255))
    click_agent = db.Column(db.String(255))
    time_clicked = db.Column(db.DateTime)
    link_id = db.Column(db.Integer, db.ForeignKey('link.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    clicker_id = db.Column(db.Integer, db.ForeignKey('click.id'))









