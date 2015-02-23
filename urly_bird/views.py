from flask import render_template, flash, redirect, request, url_for, session
from flask.ext.login import (login_user, login_required, logout_user,
                             current_user)
from datetime import datetime
from . import app, db, shortner

from .forms import LoginForm, RegistrationForm, LinkForm
from .models import User, Link


def flash_errors(form, category="warning"):
    """Show all errors from a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}".format(
                getattr(form, field).label.text, error), category)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/add", methods=["GET", "POST"])
def add():
    form = LinkForm()
    if form.validate_on_submit():
        submission = Link(original=form.link.data,
                          title=form.title.data,
                          description=form.description.data,
                          date=datetime.utcnow(),
                          owner=current_user.id)
        db.session.add(submission)
        db.session.flush()
        submission.short = shortner.encode(submission.id)
        print(submission.id, submission.short)
        db.session.commit()
        return render_template("success.html", shorturl=submission.short)
    else:
        return render_template("add_link.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("You were logged in!")
            return redirect(request.args.get("next") or url_for("index"))
        else:
            flash("E-mail address or password invalid.")
    flash_errors(form)
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
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


@app.route("/<short>")
def redirect_to(short):
    url = Link.query.filter_by(short=short).first()
    if url:
        url = url.original
        if url.find("://") == -1:
            url = "http://" + url
        return redirect(url)
    else:
        flash("URL Not Found.")
        return redirect(url_for("index"))


@app.route("/show_all")
def show_all():
    all_links = Link.query.all()
    all_links.reverse()
    return render_template("show_all.html", links=all_links)
