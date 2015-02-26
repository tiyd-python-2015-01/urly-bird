from flask import render_template, redirect, flash, url_for, request, send_file
from flask.ext.login import login_user, login_required
from flask.ext.login import logout_user, current_user
from . import app, db
from .forms import LoginForm, RegistrationForm, AddLink, EditLink
from .models import User, Links, Click
import random
from sqlalchemy import desc
from datetime import datetime
from io import BytesIO
import matplotlib.pyplot as plt


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


@app.route('/home/stats')
@login_required
def stat_table():
    links = Links.query.filter_by(user_id=current_user.id).order_by(Links.id.desc())
    #link_data = [len(link.clicks_per_day()) for link in links]
    return render_template('stats.html', user_links=links)


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
@login_required
def edit_bookmark(id):
    current = Links.query.get(id)
    form = EditLink(obj=current)
    if form.validate_on_submit():
        form.populate_obj(current)
        db.session.commit()
        flash('Bookmark Updated')
        return redirect(url_for('home_view'))
    else:
        flash_errors(form)
    return render_template('editlink.html', form=form,
                            update_url=url_for('edit_bookmark', id=current.id))


@app.route('/delete/<int:id>', methods=['GET'])
def delete_bookmark(id):
    current = Links.query.get(id)
    db.session.delete(current)
    db.session.commit()
    flash('Bookmark Deleted!!')
    return redirect(url_for('home_view'))


@app.route('/<int:id>/data')
def link_data(id):
    link = Links.query.get_or_404(id)
    return render_template('link_data.html', link=link)

@app.route('/link/<int:id>_clicks.png/')
def link_click_chart(id):
    link = Links.query.get_or_404(id)
    link_data = link.clicks_per_day()
    dates = [c[0] for c in link_data]
    click_count = [c[1] for c in link_data]
    date_labels = [d.strftime("%b %d") for d in dates]
    every_other_date_label = [d if i % 2 else ""
                              for i, d in enumerate(date_labels)]


    fig = BytesIO()
    plt.plot_date(x=dates, y=click_count, fmt='-')
    plt.xticks(dates, every_other_date_label, rotation=45, size="x-small")
    plt.savefig(fig)
    plt.clf()
    fig.seek(0)
    return send_file(fig, mimetype='image/png')


def short():
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMOPQRSTUVWXYZ0123456789'
    tag = ''.join(random.sample(chars, 6))
    short = Links.query.filter_by(short=tag).first()
    if short:
        return short()
    else:
        return tag


@app.route('/b/<tag>')
def redirect_tag(tag):
    short = tag
    actual = Links.query.filter_by(short=short).first()
    if current_user.is_authenticated():
        click = Click(user_id=current_user.id,
                      link_id=actual.id,
                      timestamp=datetime.utcnow(),
                      ip=request.remote_addr,
                      user_agent=request.headers.get('User-Agent'))
        db.session.add(click)
        db.session.commit()
    else:
        click = Click(user_id = 0,
                      link_id=actual.id,
                      timestamp=datetime.utcnow(),
                      ip=request.remote_addr,
                      user_agent=request.headers.get('User-Agent'))
        db.session.add(click)
        db.session.commit()
    return redirect(actual.url)
