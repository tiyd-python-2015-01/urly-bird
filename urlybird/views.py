from flask import render_template, flash, request, url_for, redirect
from flask.ext.login import login_user, logout_user, login_required, current_user
from .forms import LoginForm, RegisterForm, CreateLinkForm, CustomLinkForm
from . import app, db
from .models import User, Link, Custom, Click
from datetime import datetime
from sqlalchemy import desc
import plotly.plotly as py
from plotly.graph_objs import*

py.sign_in('bodandly', 'plmh01cnfk')


def flash_errors(form, category="warning"):
    '''Flash all errors for a form.'''
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}".format(getattr(form, field).label.text, error), category)


@app.route('/')
def index():
    links = Link.query.order_by(Link.id).all()

    return render_template('index.html', links=links, base_url=request.url_root)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.name.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Logged in successfully.")
            return redirect(request.args.get('next') or url_for("index"))
        else:
            flash("That user name or password is not correct.")
    flash_errors(form)

    return render_template('login.html', form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.name.data).first()
        if user:
            flash("A user with that user name already exists.")
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

    return render_template("registration.html", form=form)


@app.route('/<small_link>', methods=["GET"])
def redirect_link(small_link):
    link = Link.query.filter(Link.short_link == small_link).first()
    link_owner = Link.query.filter(User.id == link.user_id).first()
    user = current_user
    big_link = link.long_link
    if user.is_active():
        click = Click(ip_address=request.remote_addr,
                      click_agent=request.headers.get('User-Agent'),
                      time_clicked=datetime.now(),
                      link_id=link.id,
                      user_id=link_owner.id,
                      clicker_id=user.id)
        db.session.add(click)
        db.session.commit()
        return redirect(big_link)

    elif user.is_anonymous:
        click = Click(ip_address=request.remote_addr,
                      click_agent=request.headers.get('User-Agent'),
                      time_clicked=datetime.now(),
                      link_id=link.id,
                      user_id=link_owner.id,
                      clicker_id=0)
        db.session.add(click)
        db.session.commit()
        return redirect(big_link)

    return redirect(big_link)


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    flash("You have been logged out")

    return redirect(url_for('index'))


@app.route("/create_link", methods=["GET", "POST"])
@login_required
def create_link():
    form = CreateLinkForm()
    if form.validate_on_submit():
        link = Link(user=current_user, **form.data)
        link.set_short_link()
        db.session.add(link)
        db.session.commit()
        flash("You've created a new link!")
        return redirect(url_for('create_link'))
    else:
        flash_errors(form)

    return render_template("create_link.html", form=form)


@app.route('/show_links', methods=["GET", "POST"])
@login_required
def show_links():
    user = current_user.id
    links = Link.query.filter(Link.user_id == user).order_by(Link.id.desc())

    return render_template('show_links.html', links=links, base_url=request.url_root)


@app.route('/change_link/<small_link>', methods=["GET", "POST"])
@login_required
def customize_link(small_link):
    form = CustomLinkForm()
    old_link = Link.query.filter(Link.short_link == small_link).first()
    if form.validate_on_submit():
        new_link = Custom(link=old_link.short_link, new_link=form.custom_link.data)
        db.session.add(new_link)
        db.session.commit()
        flash("You've customized your link!")
        return redirect(url_for('show_links'))
    else:
        flash_errors(form)

    return render_template("custom_link.html", form=form,
                           update_url=url_for('customize_link',
                                              small_link=old_link.short_link))


@app.route('/delete_link/<small_link>', methods=["GET"])
@login_required
def delete_link(small_link):
    link = Link.query.filter(Link.short_link == small_link).first()
    db.session.delete(link)
    db.session.commit()

    return redirect(url_for('show_links'))


@app.route('/edit/<small_link>', methods=["GET", "POST"])
@login_required
def edit_link(small_link):
    note_link = Link.query.filter(Link.short_link == small_link).first()
    form = CreateLinkForm(obj=note_link)
    if form.validate_on_submit():
        form.populate_obj(note_link)
        db.session.commit()
        flash("Your edits have been made.")
        return redirect(url_for('show_links'))
    else:
        flash_errors(form)

    return render_template("edit_link.html", form=form,
                           update_url=url_for('edit_link',
                                              small_link=note_link.short_link))

@app.route('/show_link_stats', methods=["GET"])
@login_required
def show_stats():
    user = current_user
    clicks = Click.query.filter(Click.user_id == user.id).all()
    return render_template('show_stats.html', clicks=clicks)

@app.route('/show_chart/<small_link>')
def make_clicks_chart(small_link):
    chart_link = Link.query.filter(Link.short_link == small_link).first()
    click_data = chart_link.clicks_by_day()
    dates = [c[0] for c in click_data]
    num_clicks = [c[1] for c in click_data]
    date_labels = [d.strftime("%b %d") for d in dates]
    click_chart = Scatter(
    x=date_labels,
    y=num_clicks)
    data = Data([click_chart])
    chart_url = py.plot(data)
    return render_template('chart_data.html', chart_url=chart_url)