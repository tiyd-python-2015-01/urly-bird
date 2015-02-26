from flask import Blueprint, render_template, flash, redirect, request, url_for, send_file
from flask.ext.login import login_user, logout_user, current_user, login_required

from ..extensions import db
from ..forms import LoginForm, RegistrationForm, BookmarkForm
from ..models import User, Bookmark, Click

from hashids import Hashids
import random
from datetime import datetime
from io import BytesIO
import matplotlib.pyplot as plt

bookmarks = Blueprint("bookmarks", __name__)

def flash_errors(form, category="warning"):
    '''Flash all errors for a form.'''
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}".format(getattr(form, field).label.text, error), category)


@bookmarks.route("/")
def index():
    bookmark_list = Bookmark.query.all()
    return render_template("index.html", bookmark_list=reversed(bookmark_list))

@bookmarks.route("/logged_in")
@login_required
def logged_in():
    bookmark_list = Bookmark.query.filter_by(user = current_user).all()
    return render_template("logged_in.html", bookmark_list=reversed(bookmark_list))


@bookmarks.route("/bookmark", methods=["GET", "POST"])
@login_required
def bookmark():
    form = BookmarkForm()
    bookmark_list = Bookmark.query.all()
    if form.validate_on_submit():
        short_bookmark = hasher()
        bookmark = Bookmark(longurl=form.longurl.data,
                    shorturl=short_bookmark,
                    title=form.title.data,
                    summary=form.summary.data,
                    user_id=current_user.id)
        db.session.add(bookmark)
        db.session.commit()
        return redirect(url_for("bookmarks.logged_in"))
    flash_errors(form)
    return render_template("bookmark.html", form=form)

def hasher():
    hashids = Hashids(salt='salty salt')
    x = random.randint(100000, 999999)
    y = hashids.encrypt(x)
    return y

@bookmarks.route('/<shorturl>', methods = ["GET"])
def go_to_bookmark(shorturl):
    a_link = Bookmark.query.filter_by(shorturl=shorturl).first()
    click = Click(bookmark = a_link,
                  click_date = datetime.now(),
                  user = current_user)
    db.session.add(click)
    db.session.commit()
    return redirect(a_link.longurl, code = 301)

@bookmarks.route("/bookmark/<int:id>/data")
def bookmark_data(id):
    bookmark =  Bookmark.query.get_or_404(id)
    return render_template("bookmark_data.html", bookmark=bookmark)

@bookmarks.route("/bookmark/<int:id>_clicks.png")
def bookmark_clicks_chart(id):
    bookmark = Bookmark.query.get_or_404(id)
    click_data = bookmark.clicks_by_day()
    dates = [c[0] for c in click_data]
    num_clicks = [c[1] for c in click_data]

    fig = BytesIO()
    plt.plot_date(x=dates, y=num_clicks, fmt="-")
    plt.savefig(fig)
    plt.clf()
    fig.seek(0)
    return send_file(fig, mimetype="image/png")
