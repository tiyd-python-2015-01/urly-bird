from flask import render_template, flash, redirect, request, url_for
from flask.ext.login import login_user, logout_user, current_user, login_required

from . import app, db
from .forms import LoginForm, RegistrationForm, BookmarkForm
from .models import User, Bookmark, Click

from hashids import Hashids
import random
from datetime import datetime


def flash_errors(form, category="warning"):
    '''Flash all errors for a form.'''
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}".format(getattr(form, field).label.text, error), category)


@app.route("/")
def index():
    bookmark_list = Bookmark.query.all()
    return render_template("index.html", bookmark_list=reversed(bookmark_list))

@app.route("/logged_in")
@login_required
def logged_in():
    bookmark_list = Bookmark.query.filter_by(user = current_user).all()
    return render_template("logged_in.html", bookmark_list=reversed(bookmark_list))


@app.route("/bookmark", methods=["GET", "POST"])
@login_required
def bookmark():
    form = BookmarkForm()
    bookmark_list = Bookmark.query.all()
    if form.validate_on_submit():
        short_bookmark = hasher()
        bookmark = Bookmark(longurl=form.longurl.data,
                    shorturl=short_bookmark,
                    title=form.title.data,
                    summary=form.summary.data,
                    user_id=current_user.id)
        db.session.add(bookmark)
        db.session.commit()
        return redirect(url_for("logged_in"))
    flash_errors(form)
    return render_template("bookmark.html", form=form)

def hasher():
    hashids = Hashids(salt='salty salt')
    x = random.randint(100000, 999999)
    y = hashids.encrypt(x)
    return y

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Logged in successfully.")
            return redirect(request.args.get("next") or url_for("logged_in"))
        else:
            flash("That email or password is not correct.")

    flash_errors(form)
    return render_template("login.html", form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash("A user with that email address already exists.")
        else:
            user = User(name=form.name.data,
                        email=form.email.data,
                        password=form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash("You have been registered and logged in.")
            return redirect(url_for("logged_in"))
    else:
        flash_errors(form)
    return render_template("register.html", form=form)

@app.route('/<shorturl>', methods = ["GET"])
def go_to_bookmark(shorturl):
    a_link = Bookmark.query.filter_by(shorturl=shorturl).first()
    click = Click(bookmark = a_link,
                  click_date = datetime.utcnow(),
                  user = current_user)
    db.session.add(click)
    db.session.commit()
    return redirect(a_link.longurl, code = 301)
