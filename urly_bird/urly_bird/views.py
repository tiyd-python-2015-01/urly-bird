from flask import render_template, flash, redirect, request, url_for
from .extensions import db
from .app import app
from . import models
from .utils import flash_errors
from .forms import RegistrationForm, LoginForm
from flask.ext.login import login_user, login_required, logout_user, current_user

"""Add your views here."""


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect("login.html")


@app.route("/")
def home():
    return render_template("layout.html")


@app.route("/index", methods=["POST"])
@login_required
def index():
    return render_template("layout.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(email=form.email.data)
        if user and models.User.check_password(form.password.data):
            login_user(user)
            flash("Logged in successfully.")
            return redirect(request.args.get("next") or url_for("index"))
        else:
            flash("That email or password is not correct.")

    flash_errors(form)
    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(email=form.email.data)
        if user:
            flash("E-mail address already in use.")
        else:
            user = models.User(name=form.name.data,
                        email=form.email.data,
                        password=form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            db.session["username"] = user.name
            flash("Registration Successful!  You have been logged in.")
            return redirect(url_for("/"))
    else:
        flash_errors(form)
    return render_template("register.html", form=form)
