from flask import render_template, flash, redirect, request, url_for, send_file
from flask.ext.login import login_user , login_required, current_user
from flask.ext.login import logout_user
from . import app, db
from .forms import LoginForm, RegistrationForm, ShortenLink
from .models import User, Bookmark, Click
from hashids import Hashids
from random import randint
from datetime import datetime
from sqlalchemy import desc
from io import BytesIO
import matplotlib.pyplot as plt


hashids = Hashids(salt = "a nice salt")

def shortener():
    rand_list = [randint(1,10) for _ in range(3)]
    id = hashids.encode(*rand_list)
    return id

@app.route("/", methods = ["GET"])
def index():
    links = Bookmark.query.order_by(Bookmark.sub_date.desc()).limit(5)
    return render_template("index.html", links = links)

def flash_errors(form, category="warning"):
    '''Flash all errors for a form.'''
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}".format(getattr(form, field).label.text, error), category)


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

@app.route("/user_page", methods = ["GET", "POST"])
@login_required
def shorten_link():
    form = ShortenLink()
    links = Bookmark.query.filter_by(user = current_user).all()
    if form.validate_on_submit():
        bookmark = Bookmark(url = form.url.data,
                            title = form.title.data,
                            shortlink =  shortener(),
                            user = current_user,
                            sub_date = datetime.utcnow(),
                            )
        db.session.add(bookmark)
        db.session.commit()
        flash("Link added")
        return redirect(url_for("shorten_link"))

    return render_template("user_page.html", form=form, links = links)



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


@app.route("/logoff", methods = ["GET"])
def logoff():
    logout_user()
    return redirect(url_for("index"))

@app.route('/<shortlink>', methods = ["GET"])
def go_to_bookmark(shortlink):
    the_link = Bookmark.query.filter_by(shortlink=shortlink).first()
    click = Click(bookmark = the_link,
                  click_date = datetime.utcnow(),
                  user = current_user)
    db.session.add(click)
    db.session.commit()
    return redirect("http://"+the_link.url, code = 301)

@app.route("/delete", methods = ["POST"])
def rm_bookmark():
    link = Bookmark.query.filter_by(shortlink=request.form['link_to_delete']).first()
    db.session.delete(link)
    db.session.commit()
    return redirect(url_for("shorten_link"))


@app.route("/user_page/<int:id>", methods=["GET", "POST"])
@login_required
def edit_link(id):
    link = Bookmark.query.get(id)
    form = ShortenLink(obj=link)
    if form.validate_on_submit():
        form.populate_obj(link)
        db.session.add(link)
        db.session.commit()
        flash("The link has been updated.")
        return redirect(url_for("shorten_link"))

    return render_template("edit.html",
                           form=form,
                           post_url=url_for("edit_link", id=link.id),
                           button="Update Link")

@app.route("/link_data/<int:id>", methods=["GET", "POST"])
def show_data(id):
    clicks = Click.query.filter_by(bookmark_id = id).all()
    bookmark = Bookmark.query.filter_by(id = id).first()
    return render_template("show_data.html", clicks = clicks, bookmark = bookmark)


@app.route("/link_data/<int:id>_clicks.png")
def book_clicks_chart(id):

    bookmark = Bookmark.query.filter_by(id = id).first()
    click_data = bookmark.clicks_by_day()
    dates = [c[0] for c in click_data]
    num_clicks = [c[1] for c in click_data]

    fig = BytesIO()
    plt.plot(x=dates, y=num_clicks, fmt="-")
    plt.savefig(fig)
    plt.clf()
    fig.seek(0)
    return send_file(fig, mimetype="image/png")
