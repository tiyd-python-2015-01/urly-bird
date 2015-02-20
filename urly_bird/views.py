from flask import render_template, flash, redirect, request, url_for, session
from flask.ext.login import login_user, login_required, logout_user
from . import app, db

from .forms import LoginForm, RegistrationForm, LinkForm
from .models import User


def flash_errors(form, category="warning"):
    """Show all errors from a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}".format(
                getattr(form, field).label.text, error), category)


@app.route("/")
def index():
    form = LinkForm()
    return render_template("index.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            session["username"] = user.name
            flash("You were logged in!")
            return redirect(request.args.get("next") or url_for("index"))
        else:
            flash("E-mail address or password invalid.")
    flash_errors(form)
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    session.pop('username', None)
    logout_user()
    return redirect(url_for("index"))


@app.route("/create_user", methods=["GET", "POST"])
def create_user():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash("E-mail address already in use.")
        else:
            user = User(name=form.name.data,
                        email=form.email.data,
                        password=form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            session["username"] = user.name
            flash("Registration Successful!  You have been logged in.")
            return redirect(url_for("index"))
    else:
        flash_errors(form)
    return render_template("register.html", form=form)

    
@app.route("/shorten", methods=["POST"])
def shorten():
    pass
