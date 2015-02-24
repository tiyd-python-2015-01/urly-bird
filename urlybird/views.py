from flask import render_template, flash, redirect, request, url_for, request
from flask.ext.login import login_user, logout_user
from flask.ext.login import login_required, current_user

from .app import app, db
from .forms import LoginForm, RegistrationForm, AddBookmark
from .models import Bookmark, User, BookmarkUser, Click
from datetime import datetime
from sqlalchemy import desc, and_
import random


def flash_errors(form, category="warning"):
    '''Flash all errors for a form.'''
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}".format(getattr(form,
                  field).label.text, error), category)


@app.route("/", defaults={'page': 1})
@app.route('/<int:page>')
def index(page):
    top_bookmarks = BookmarkUser.query.order_by(desc(BookmarkUser.id))[:10]
    return render_template("index.html", bookmarks=top_bookmarks)

@app.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    form = AddBookmark()
    user = current_user.name.capitalize()
    bookmarks = BookmarkUser.query.filter_by(user_id=current_user.id).all()
    return render_template("dashboard.html",
                           bookmarks=bookmarks,
                           form=form,
                           user=user)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for("dashboard"))
        else:
            flash("That email or password is not correct.")

    flash_errors(form)
    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

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
            return redirect(url_for("dashboard"))
    else:
        flash_errors(form)

    return render_template("register.html", form=form)

@app.route('/dashboard/add_bookmark', methods=['POST'])
@login_required
def add_bookmark():
    form = AddBookmark()
    if form.validate_on_submit():
        url_list = BookmarkUser.query.filter_by(user_id=current_user.id).all()

        url = [item.id for item in url_list if item.item_id==form.url.data]

        if url:
            flash("You've already shortened that URL!")
        else:
            shortened_url = shorten_url(url)
            bookmark = Bookmark(title=form.title.data,
                                url=form.url.data,
                                short_url=shortened_url,
                                description=form.description.data)
            db.session.add(bookmark)
            db.session.commit()
            bookmark_id = Bookmark.query.filter_by(short_url=shortened_url).first()
            user_bookmark = BookmarkUser(user_id=current_user.id,
                                          item_id=bookmark_id.id)
            db.session.add(user_bookmark)
            db.session.commit()
            flash("You successfully added a link")
            return redirect(url_for('dashboard'))
    else:
        flash_errors(form)

    return redirect(url_for('dashboard'))

@app.route('/b/<short_url>')
def url_redirect(short_url):
    correct_url = Bookmark.query.filter_by(short_url=short_url).first()
    if correct_url:
        bookmark_user = BookmarkUser.query.filter_by(item_id=correct_url.id).first()
        add_click(correct_url.id)
        return redirect(correct_url.url)
    else:
        return redirect(url_for('/'))

@app.route('/dashboard/r/<int:int_id>', methods=["GET"])
@login_required
def delete_bookmark(int_id):
    deleted_object = BookmarkUser.query.filter_by(id=int_id).first()
    db.session.delete(deleted_object)
    db.session.commit()
    flash("You successfully removed that link")
    return redirect(url_for('dashboard'))

@app.route('/dashboard/e/<int:int_id>', methods=['POST', 'GET'])
@login_required
def edit_bookmark(int_id):
    form = AddBookmark()
    edited_object = BookmarkUser.query.filter_by(id=int_id).first()

    if form.validate_on_submit():
        edited_object.bookmark.title = form.title.data
        edited_object.bookmark.url = form.url.data
        edited_object.bookmark.short_url = shorten_url(form.url.data)
        edited_object.bookmark.description = form.description.data
        db.session.commit()
        flash("You successfully updated your bookmark")
        return redirect(url_for('dashboard'))
    else:
        flash_errors(form)
        return render_template("edit.html",
                               form=form,
                               edited_object=edited_object)

def shorten_url(a_url):
    alphabet = list('abcdefghijklmnopqrstuvwxyz1234567890')
    shortened_url = ''.join(random.sample(alphabet, 6))
    existing_url = Bookmark.query.filter_by(short_url=shortened_url).first()
    if shortened_url == existing_url:
        return shorten_url(a_url)
    else:
        return shortened_url

def add_click(bookmark_id):
    print(request.headers.get('User-Agent'))
    if current_user.is_active():
        user = current_user.id
    else:
        user = 0

    click = Click(item_id=bookmark_id,
                  user_id=user,
                  timestamp=datetime.utcnow(),
                  user_ip_address=request.remote_addr,
                  user_agent=request.headers.get('User-Agent'))
    db.session.add(click)
    db.session.commit()
