from flask import render_template, flash, redirect, request, url_for
from flask.ext.login import login_user, login_required, logout_user, current_user
from . import db, app
from .forms import LoginForm, RegistrationForm, CreateLinkForm
from .models import User, Link
from datetime import datetime


def flash_errors(form, category="warning"):
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}".format(getattr(form, field).label.text, error), category)


@app.route("/")
def index():
    form = LoginForm()
    return render_template("index.html", form=form)


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
            flash("The email or password you entered is not correct.")

    flash_errors(form)
    return render_template("login.html", form=form)


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
            flash("Thank you for registering. You are now logged in.")
            return redirect(url_for("index"))
    else:
        flash_errors(form)

    return render_template("register.html", form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You have been logged out")
    return redirect(url_for('index'))


@app.route('/shorten', methods=['GET', 'POST'])
def shorten():
    form = CreateLinkForm()
    if request.method == 'POST':
        url_input = form.link.data
        link = Link(original_link=url_input)
        link.description = form.description.data
        link.date = datetime.now()
        link.user = current_user
        db.session.add(link)
        db.session.commit()
        link.shorten_url()
        db.session.commit()
        return render_template("add_link.html", short_link=link.short_link, form=form)
    return render_template("add_link.html", form=form)


@app.route('/<hashid>')
def go_to_short_link(hashid):
    link = Link.query.filter(Link.short_link == hashid).first()
    if link:
        return redirect(link.original_link)
    else:
        flash("Link not found.")
        return redirect(url_for('index'))
