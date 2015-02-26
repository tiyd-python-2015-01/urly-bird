from flask import Blueprint, render_template, flash, redirect, request, url_for
from flask.ext.login import login_user, logout_user

from ..extensions import db
from ..forms import LoginForm, RegistrationForm
from ..models import User

users = Blueprint("users", __name__)

@users.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(request.args.get("next") or url_for("linksb.index"))
        else:
            flash("That email or password is not correct.")
            return redirect(url_for("users.register"))
    return render_template("login.html", form=form)


@users.route("/logout", methods=["GET","POST"])
def logout():
    logout_user()
    return redirect(url_for("linksb.index"))


@users.route("/register", methods=["GET", "POST"])
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
            return redirect(url_for("linksb.index"))
    return render_template("register.html", form=form)
