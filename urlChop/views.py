from flask import render_template, flash, redirect, request, url_for
from flask.ext.login import login_user, logout_user, login_required, current_user

from . import app, db
from .forms import LoginForm, RegistrationForm, Newlink
from .models import User, Links, UserLinks
import random


def flash_errors(form, category="warning"):
    '''Flash all errors for a form.'''
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}".format(getattr(form, field).label.text, error), category)


@app.route("/")
def index():
    links = Links.query.all()
    return render_template("index.html", links=links)


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

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/register", methods=["GET", "POST"])
def register():
    #user = current_user (THIS IS A FLASK TOKEN)
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash("A user with that email address already exists.")
        else:
            #link = Links(user = current_user.id, longlink=form.adderss.data)
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

@app.route("/add_link", methods=["GET", "POST"])
# @login_required
def add_link():
    #user = current_user #(THIS IS A FLASK TOKEN)
    form = Newlink()
    if form.validate_on_submit():
        url = Links.query.filter_by(url=form.url.data).first()
        if url:
            flash("You already have a link made for that URL")
        else:
            chopped = chopper(url)
            link = Links(user = current_user.id,
                        url=form.url.data,
                        shortlink=chopped,
                        description=form.description.data)
            db.session.add(link)
            db.session.commit()
            #login_user(user)
            flash("You added a new choppedURL.")
            return redirect(url_for("index"))
    else:
        flash_errors(form)

    return redirect(url_for('index'))

# Clinton's Friday freeshelf example
# @app.route("/favorite", methods=["POST"])
# @login_required
# def add_favorite():
#     book_id = request.form['book_id']
#     book = Book.query.get(book_id)
#     favorite = Favorite(user=current_user, book=book)
#     db.session.add(favorite)
#     db.session.commit()
#     flash("You have added {} as a favorite.".format(book.title))
#     return redirect(url_for("index"))



def chopper(anyurl):
    alpha = list('abcdefghijklmnopqrstuvwxyz\
                  ABCDEFGHIJKLMNOPQRSTUVWXYZ\
                  1234567890')
    shortlink = ''.join(random.sample(alpha, 5))
    existing = Links.query.filter_by(shortlink=shortlink).first()
    if shortlink == existing:
        return chopper(anyurl)
    else:
        return shortlink
