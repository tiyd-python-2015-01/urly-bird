from flask import render_template, redirect, request, url_for
from .forms import UrlForm, RegisterUser, Login
from .models import BookmarkedUrl
from . import app, db
from hashids import Hashids


@app.route('/')
def index():
    new_url_form = UrlForm()
    return render_template('index.html', new_url_form=new_url_form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    new_login = Login()
    return render_template('login.html', new_login=new_login)


@app.route('/logout', methods=['POST'])
def logout():
    return redirect(url_for('index'))


@app.route('/register', methods=['Get', 'POST'])
def register():
    new_registration_form = RegisterUser()
    return render_template('register.html',
                            new_registration_form=new_registration_form)


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


@app.route('/go/<shorturl>')
def send_to_url(shorturl):
    long_url = BookmarkedURL.query.get(shorturl)
    return redirect(long_url)
