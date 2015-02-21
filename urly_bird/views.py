from datetime import datetime
"""Add your views here."""

from flask import render_template, flash, redirect, request, url_for
from flask.ext.login import login_user, logout_user, login_required, current_user

from .app import app, db,  login_manager
from .forms import LoginForm, RegistrationForm, LinkAddForm
from .models import User, Links
from .utils import flash_errors


def flash_errors(form, category="warning"):
    '''Flash all errors for a form.'''
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}".format(getattr(form, field).label.text, error), category)


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


@app.route("/")
def index():
    if current_user.is_authenticated():
        links = Links.query.filter_by(user=current_user.id).order_by(Links.id.desc())
        return render_template("index.html",links=links)
    else:
        return render_template("index.html",links=[])


@app.route("/links")
@login_required
def links():
    links = Links.query.filter_by(user=current_user.id).order_by(Links.id.desc())
    return render_template("links.html",links=links)

@app.route("/all_links")
def all_links():
    links = Links.query.order_by(Links.id.desc()).all()
    return render_template("index.html",links=links)



@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            links = Links.query.filter_by(user=current_user.id).order_by(Links.id.desc())
            return render_template("index.html",links=links)
        else:
            flash("That email or password is not correct.")
    flash_errors(form)
    return render_template("login.html", form=form)


@app.route('//urly/<path:new_url>')
def show_link(new_url):
    link = Links.query.filter_by(short=new_url).first()
    cl_user = current_user.id
    cl_time = datetime.utc_now()
    cl_link = link.id
    new_click = Clicks(user_id=current_user,
                       link_id = link,
                       when = datetime.utc_now())
    db.session.add(new_click)
    db.session.commit()
    flash("click is in")
    return redirect(url_for(link.long))


@app.route("/logout", methods=["GET","POST"])
def logout():
    logout_user()
    return redirect(url_for("index"))


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


@app.route("/add_link", methods=["GET", "POST"])
@login_required
def add_link():
    form = LinkAddForm()
    if form.validate_on_submit():
        new_link = Links(long=form.long.data,
                   title=form.title.data,
                   description=form.description.data)



        last_id = db.session.query(db.func.max(Links.id)).scalar()
        if not last_id:
            last_id=0
        new_link.set_short(last_id+1)
        new_link.user = current_user.id
        db.session.add(new_link)
        db.session.commit()
        return redirect(url_for("index"))
    else:
        flash_errors(form)
    return render_template("add_link.html", form=form)
