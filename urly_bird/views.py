import re
import random
from io import BytesIO
from datetime import datetime
from flask import render_template, flash, redirect, request, url_for, send_file
from flask.ext.login import login_user, login_required, current_user, logout_user
from hashids import Hashids
from .app import app, db
from .forms import LoginForm, RegistrationForm, URLForm
from .models import URL, User, Timestamp
from .utils import flash_errors
from .stats import create_plot

@app.route("/")
def index():
    if not current_user.is_authenticated():
        urls = URL.query.all()
        return render_template("index.html", urls=reversed(urls[-5::]), domain=request.url_root)
    return redirect(url_for("user"))


@app.route("/user", methods=['GET', 'POST'])
@login_required
def user():
    url_list = URL.query.filter_by(owner=current_user.id)
    form = URLForm()
    #edit_address(form.address)
    if form.validate_on_submit():
        url = URL.query.filter_by(long_address=form.address.data).first()
        if url:
            flash("You've already made a bookmark for this url.")
        else:
            url = URL(name=form.title.data,
                      description=form.description.data,
                      long_address=form.address.data,
                      owner=current_user.id,
                      clicks=0)
            db.session.add(url)
            # Once the url is added, we have its unique, numerical id.
            # Encode that id so that it becomes a short string and append it to the url.
            # Also check for redundant hashes so that we can match short addresses to users
            # Set the short_address attribute and commit.
            hashed_url = URL.query.filter_by(long_address=form.address.data).first()
            salt = "seasalt{}".format(current_user.id)
            hashed_id = Hashids(salt=salt, min_length=4).encode(hashed_url.id)
            while len(URL.query.filter_by(short_address=hashed_id).all()) > 0:
                salt = "seasalt{}".format(random.randint())
                hashed_id = Hashids(salt=salt, min_length=4).encode(hashed_url.id)
            hashed_url.short_address = hashed_id
            db.session.commit()
            flash("URL added!")
            return redirect(url_for("index"))
    elif request.method == 'POST':
        flash("Error adding URL.")
    return render_template("user.html", form=form, urls=url_list, domain=request.url_root)


@app.route("/register", methods=['GET', 'POST'])
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


@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    print("Logged Out")
    logout_user()
    return redirect("/")


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Logged in successfully.")
            return redirect(request.args.get("next") or url_for("index"))
        else:
            flash("Email or password is incorrect")
    flash_errors(form)
    return render_template("login.html", form=form)


@app.route('/b/<shorty>')
def route(shorty):
    url = URL.query.filter_by(short_address=shorty).first()
    timestamp = Timestamp(url_id=url.id,
                          timestamp=datetime.utcnow(),
                          ip_address=request.remote_addr,
                          user_agent=request.headers.get('User-Agent'))
    db.session.add(timestamp)
    url.clicks += 1
    db.session.commit()
    return redirect(url.long_address)

@app.route('/e/<shorty>', methods=['GET','POST'])
@login_required
def edit(shorty):
    url = URL.query.filter_by(short_address=shorty).first()
    form = URLForm(title=url.name, description=url.description, address=url.long_address)
    if url and url.owner == current_user.id:
        if request.method == 'GET':
            return render_template("link.html", url=url, form=form)
        elif request.method == 'POST':
            url.name = form.title.data
            url.long_address = form.address.data
            url.description = form.description.data
            db.session.commit()
            flash("Saved!")
    # Anything that fails the above if statements falls through to return index.html
    return redirect(url_for("index"))

@app.route('/s/<shorty>')
def stats(shorty):
    url = URL.query.filter_by(short_address=shorty).first_or_404()
    fig = create_plot(url.id)
    return send_file(fig, mimetype="image/png")



@app.route('/d/<shorty>')
def delete(shorty):
    url = URL.query.filter_by(short_address=shorty).first()
    if url:
        db.session.delete(url)
        db.session.commit()
    return redirect(url_for("index"))


def edit_address(address):
    if address.data and not re.match(r'^(http://)', address.data):
        address.data = "http://{}".format(address.data)
