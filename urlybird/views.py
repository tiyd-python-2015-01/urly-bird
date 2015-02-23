from flask import render_template, flash, redirect, request, url_for
from flask.ext.login import login_user, logout_user, current_user, login_required

from . import app, db
from .forms import LoginForm, RegistrationForm, BookmarkForm, BookForm
from .models import Book, User, Bookmark

from hashids import Hashids


def flash_errors(form, category="warning"):
    '''Flash all errors for a form.'''
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}".format(getattr(form, field).label.text, error), category)


@app.route("/")
def index():
    books = Book.query.all()
    return render_template("index.html", books=books)

@app.route("/book", methods=["GET", "POST"])
def book():
    form = BookForm()
    book = Book(title=form.title.data,
                description=form.description.data,
                url=form.url.data)
    db.session.add(book)
    db.session.commit()
    flash("Your book was created.")
    # else:
    #     flash("Your book could not be created.")
    # books = Book.query.all()
    # return render_template("book.html", books=books)


@app.route("/bookmark", methods=["GET", "POST"])
def bookmark():
    form = BookmarkForm()

    bookmark = Bookmark(longurl=form.longurl.data,
                title=form.title.data,
                summary=form.summary.data)
    bookmark_list = Bookmark.query.all()
    return render_template("bookmark.html", form=form, bookmark_list=bookmark_list)


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
            return redirect(url_for("index"))
    else:
        flash_errors(form)

    return render_template("register.html", form=form)
