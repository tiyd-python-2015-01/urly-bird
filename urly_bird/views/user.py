from flask import render_template, flash, redirect, request, url_for, Blueprint
from flask.ext.login import login_user, login_required, logout_user, current_user
from datetime import datetime
from sqlalchemy import desc, func
import matplotlib.pyplot as plt
from io import BytesIO


from . import app, db
from .forms import LoginForm, RegistrationForm, URLForm, editURL
from .models import User, Link, Click

user_blueprint = Blueprint('user_blueprint', __name__,
                           template_folder='templates')

def flash_errors(form, category="warning"):
    '''Flash all errors for a form.'''
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}".format(getattr(form, field).label.text, error), category)


@user_blueprint.route("/")
def index():
    return render_template('layout.html')

@user_blueprint.route("/your_links")
def your_links():
    links = current_user.links.order_by(desc(Link.date)).all()

    return render_template('showAll.html', links=links)


@user_blueprint.route("/login", methods=["GET", "POST"])
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


@user_blueprint.route("/register", methods=["GET", "POST"])
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


@user_blueprint.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You have been logged out")
    return redirect(url_for('index'))

@user_blueprint.route('/shorten', methods=['GET', 'POST'])
@login_required
def shorten():
    form = URLForm()
    if request.method == 'POST':
        url_input = form.url.data
        link = Link(original_link = url_input)
        link.description = form.description.data
        link.date = datetime.now()
        link.user = current_user
        db.session.add(link)
        db.session.commit()
        link.get_short_link()
        db.session.commit()
        return render_template("shorten.html", short_link=link.short_link, form=form)
    return render_template("shorten.html", form=form)

@user_blueprint.route('/<hashid>')
@login_required
def short_link(hashid):
    link = Link.query.filter(Link.short_link == hashid).first()
    if link:
        click = Click(user_id=current_user.id,
                      link_id=link.id,
                      date = datetime.now())
        db.session.add(click)
        db.session.commit()
        return redirect(link.original_link)
    else:
        flash("Couldn't find link!")
        return redirect(url_for('index'))




