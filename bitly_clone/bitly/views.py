from flask import render_template, flash, redirect, request, url_for
from flask.ext.login import login_user , login_required, current_user
from flask.ext.login import logout_user
from . import app, db
from .forms import LoginForm, RegistrationForm, ShortenLink
from .models import User, Bookmark
from hashids import Hashids
from random import randint

hashids = Hashids(salt = "a nice salt")

def shortener():
    rand_list = [randint(1,10) for _ in range(3)]
    id = hashids.encode(*rand_list)
    return id

@app.route("/")
def index():
    return render_template("index.html")

def flash_errors(form, category="warning"):
    '''Flash all errors for a form.'''
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}".format(getattr(form, field).label.text, error), category)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Logged in successfully.")
            return redirect(request.args.get("next") or url_for("index"))
        else:
            flash("That email or password is not correct.")

    flash_errors(form)
    return render_template("login.html", form=form)

@app.route("/user_page", methods = ["GET", "POST"])
@login_required
def shorten_link():
    form = ShortenLink()
    links = Bookmark.query.filter_by(user = current_user).all()
    if form.validate_on_submit():
        bookmark = Bookmark(url = form.address.data,
                            title = form.title.data,
                            shortlink =  shortener(),
                            user = current_user)
        db.session.add(bookmark)
        db.session.commit()
        flash("Link added")
        return redirect(url_for("shorten_link"))

    return render_template("user_page.html", form=form, links = links)



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
            return redirect(url_for("index"))
    else:
        flash_errors(form)

    return render_template("register.html", form=form)




@app.route("/logoff", methods = ["GET"])
def logoff():
    logout_user()
    return redirect(url_for("index"))

@app.route('/<shortlink>', methods = ["GET"])
def go_to_bookmark(shortlink):
    the_link = Bookmark.query.filter_by(shortlink=shortlink).first()
    return redirect("http://"+the_link.url, code=301)
