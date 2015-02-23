from flask import render_template, redirect, flash, url_for, request
from flask.ext.login import login_user, login_required
from flask.ext.login import logout_user, current_user
from . import app, db
from .forms import LoginForm, RegistrationForm, AddLink
from .models import User, Links
import random
from sqlalchemy import desc


def flash_errors(form, category="warning"):
    '''Flash all errors for a form.'''
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}".format(getattr(form, field).label.text, error),
                                                                   category)


@app.route('/')
def index():
    link_list = Links.query.order_by(desc(Links.id)).all()
    return render_template('index.html', link_list=link_list)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('You were logged in.')
            return redirect(url_for('home_view'))
        else:
            flash('Invalid Password')

    flash_errors(form)
    return render_template('login.html', form=form)


@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    user = current_user
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))

@app.route('/home')
@login_required
def home_view():
    links = Links.query.filter_by(user_id=current_user.id).order_by(Links.id.desc())
    return render_template('home_page.html', link_list=links)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('A user with that email already exists.')
        else:
            user = User(name=form.name.data,
                        email=form.email.data,
                        password=form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash('Registration successful! You have been logged in.')
            return redirect(url_for('home_view'))
    else:
        flash_errors(form)
        return render_template('register.html', form=form)


@app.route('/addlink', methods=['GET', 'POST'])
@login_required
def add_link():
    user = current_user
    form = AddLink()
    if form.validate_on_submit():
        link = Links.query.filter_by(url=form.url.data).first()
        if link in user.links:
            flash('You already added that link.')
            flash_errors(form)
            return render_template('addlink.html', form=form)
        else:
            shorturl = short()
            link = Links(user_id = current_user.id,
                         url = form.url.data,
                         text = form.text.data,
                         short = shorturl)
            db.session.add(link)
            db.session.commit()
            flash('New Link Added')
            return redirect(url_for('home_view'))
    else:
        flash_errors(form)
        return render_template('addlink.html', form=form)


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_bookmark(id):
    current = Links.query.get(id)
    form = AddLink(obj=current)
    if form.validate_on_submit():
        form.populate_obj(current)
        db.session.commit()
        flash('Bookmark Updated')
        return redirect(url_for('home_view'))
    else:
        return render_template('editlink.html', form=form, id=id)



def short():
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMOPQRSTUVWXYZ0123456789'
    tag = ''.join(random.sample(chars, 6))
    short = Links.query.filter_by(short=tag).first()
    if short6:
        return short()
    else:
        return tag


@app.route('/b/<tag>')
def redirect_tag(tag):
    short = tag
    actual = Links.query.filter_by(short=short).first()
    return redirect(actual.url)
