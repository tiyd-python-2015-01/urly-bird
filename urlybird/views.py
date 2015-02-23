from flask import render_template, redirect, request, url_for, flash
from .forms import UrlForm, RegisterUser, Login
from .models import BookmarkedUrl, User
from . import app, db
from hashids import Hashids
from flask.ext.login import login_user, login_required, current_user, logout_user


def flash_errors(form, category="Warning"):
    """Flash multiple errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}".format(getattr(form, field).label.text, error), category)


@app.route('/')
def index():
    form = UrlForm()
    return render_template('index.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Logged in!")
            return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET','POST'])
def logout():
    logout_user()
    flash('Logged out.')
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterUser()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash("User with that email already exists.")
        else:
            user = User(name=form.name.data,
                        email=form.email.data,
                        password=form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash("You have been registered and logged in.")
            return redirect(url_for("index"))
    else: flash_errors(form)
    return render_template('register.html',
                            form=form)


@app.route('/add', methods=['POST'])
def add_url():
    hashids = Hashids()

    form = UrlForm()
    if form.validate_on_submit():
        url = BookmarkedUrl(form.text.data)
        short_url = hashids(form.text.data)
        db.session.add(url)
        db.session.commit()
    return redirect(url_for('index'))


@app.route('/shortened', methods=['POST'])
def disp_short():
    return render_template('shortened.html', url=url)


@app.route('/go/<shorturl>')
def send_to_url(shorturl):
    long_url = BookmarkedURL.query.get(shorturl)
    return redirect(long_url)
