from flask import render_template, flash, redirect, request, url_for, Blueprint
from flask.ext.login import login_user , login_required, current_user
from flask.ext.login import logout_user
from ..extensions import db
from ..forms import LoginForm, RegistrationForm, ShortenLink
from ..models import User, Bookmark, Click
from hashids import Hashids
from random import randint
from datetime import datetime
from sqlalchemy import desc
import plotly.plotly as py
from plotly.graph_objs import *

py.sign_in("dknewell1", "x0oz9ikryp")

hashids = Hashids(salt = "a nice salt")

bookmarks = Blueprint("bookmarks", __name__)

def shortener():
    rand_list = [randint(1,10) for _ in range(3)]
    id = hashids.encode(*rand_list)
    return id

@bookmarks.route("/", methods = ["GET"])
def index():
    links = Bookmark.query.order_by(Bookmark.sub_date.desc()).limit(5)
    return render_template("index.html", links = links)

def flash_errors(form, category="warning"):
    '''Flash all errors for a form.'''
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}".format(getattr(form, field).label.text, error), category)



@bookmarks.route("/user_page", methods = ["GET", "POST"])
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
        return redirect(url_for("bookmarks.shorten_link"))

    return render_template("user_page.html", form=form, links = links)


@bookmarks.route('/<shortlink>', methods = ["GET"])
def go_to_bookmark(shortlink):
    the_link = Bookmark.query.filter_by(shortlink=shortlink).first()
    click = Click(bookmark = the_link,
                  click_date = datetime.utcnow(),
                  user = current_user)
    db.session.add(click)
    db.session.commit()
    return redirect("http://"+the_link.url, code = 301)

@bookmarks.route("/delete", methods = ["POST"])
def rm_bookmark():
    link = Bookmark.query.filter_by(shortlink=request.form['link_to_delete']).first()
    db.session.delete(link)
    db.session.commit()
    return redirect(url_for("bookmarks.shorten_link"))


@bookmarks.route("/user_page/<int:id>", methods=["GET", "POST"])
@login_required
def edit_link(id):
    link = Bookmark.query.get(id)
    form = ShortenLink(obj=link)
    if form.validate_on_submit():
        form.populate_obj(link)
        db.session.add(link)
        db.session.commit()
        flash("The link has been updated.")
        return redirect(url_for("bookmarks.shorten_link"))

    return render_template("edit.html",
                           form=form,
                           post_url=url_for("boomarks.edit_link", id=link.id),
                           button="Update Link")

@bookmarks.route("/link_data/<int:id>", methods=["GET", "POST"])
def show_data(id):

    bookmark = Bookmark.query.filter_by(id = id).first()
    click_data = bookmark.clicks_by_day()
    dates = [c[0] for c in click_data]
    num_clicks = [c[1] for c in click_data]
    date_labels = [d.strftime("%b %d") for d in dates]
    click_chart = Scatter(
    x=date_labels,
    y=num_clicks)
    data = Data([click_chart])
    chart_url = py.plot(data, auto_open=False)
    return render_template('show_data.html', chart_url=chart_url, bookmark = bookmark)
