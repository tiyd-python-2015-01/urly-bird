from datetime import datetime
"""Add your views here."""

from flask import render_template, flash, redirect, request, url_for
from flask.ext.login import login_user, logout_user, login_required, current_user
import requests
from .app import app, db,  login_manager
from .forms import LoginForm, RegistrationForm, LinkAddForm, LinkUpdateForm
from .models import User, Links, Clicks
from .utils import flash_errors

import matplotlib.pyplot as plt

def flash_errors(form, category="warning"):
    '''Flash all errors for a form.'''
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}".format(getattr(form, field).label.text, error), category)


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


@app.route("/")
def index():
    if current_user.is_authenticated():
        links = Links.query.filter_by(user=current_user.id).order_by(Links.id.desc())
        return render_template("index.html",links=links)
    else:
        return render_template("index.html",links=[])


@app.route("/links")
@login_required
def links():
    links = Links.query.filter_by(user=current_user.id).order_by(Links.id.desc())
    return render_template("links.html",links=links)


@app.route("/all_links")
def all_links():
    links = Links.query.order_by(Links.id.desc()).all()
    return render_template("all_links.html",links=links)


@app.route("/add_link", methods=["GET", "POST"])
@login_required
def add_link():
    form = LinkAddForm()
    if form.validate_on_submit():
        new_link = Links(long=form.long.data,
                   title=form.title.data,
                   description=form.description.data)
        last_id = db.session.query(db.func.max(Links.id)).scalar()
        if not last_id:
            last_id=0
        new_link.set_short(last_id+1)
        new_link.user = current_user.id
        db.session.add(new_link)
        db.session.commit()
        return redirect(url_for("index"))
    else:
        flash_errors(form)
    return render_template("add_link.html", form=form)


@app.route("/delete_link/<int:id>", methods=["GET", "POST"])
def delete_link(id):
    link_id = id
    link = Links.query.get(link_id)
    db.session.delete(link)
    db.session.commit()
    links = Links.query.filter_by(user=current_user.id).order_by(Links.id.desc())
    return render_template("index.html",links=links)


@app.route('/update_link/<int:id>', methods=["GET", "POST"])
@login_required
def update_link(id):
    update_link = Links.query.get(id)
    form = LinkUpdateForm(obj=update_link)
    if form.validate_on_submit():
        form.populate_obj(update_link)
        db.session.commit()
        return redirect(url_for("index"))
    else:
        flash_errors(form)
    return render_template("update_link.html",
                            update_url = url_for("update_link",id=update_link.id),
                            form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            links = Links.query.filter_by(user=current_user.id).order_by(Links.id.desc())
            return render_template("index.html",links=links)
        else:
            flash("That email or password is not correct.")
            return redirect(url_for("register"))
    flash_errors(form)
    return render_template("login.html", form=form)


@app.route('/urly/<new_url>')
def show_link(new_url):
    link = Links.query.filter_by(short=new_url).first()
    cl_user = current_user.id
    cl_time = datetime.utcnow()
    cl_link = link.id
    new_click = Clicks(user_id=cl_user,
                       link_id=cl_link,
                       when=cl_time,
                       IP=request.remote_addr,
                       agent=request.headers.get('User-Agent'))
    db.session.add(new_click)
    db.session.commit()
    return redirect(link.long)


@app.route("/logout", methods=["GET","POST"])
def logout():
    logout_user()
    return redirect(url_for("index"))


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

@app.route("/link_clicks/<int:id>")
def link_clicks(id):
    link = Links.query.get_or_404(id)
    click_data = link.clicks_by_day()
    dates = [c[0] for c in click_data]
    num_clicks = [c[1] for c in click_data]
    plt.plot_date(x=dates, y=num_clicks,fmt='-')
    plt.savefig("/tmp/link_data.png")
    return render_template("link_data.html",
                           link=link)


#@app.route("/book/<int:id>_clicks.png")
#def book_clicks_chart(id):
#    book = Book.query.get_or_404(id)
#    click_data = book.clicks_by_day()
#    dates = [c[0] for c in click_data]
#    num_clicks = [c[1] for c in click_data]
#
#    fig = BytesIO()
#    plt.plot_date(x=dates, y=num_clicks, fmt="-")
#    plt.savefig(fig)
#    plt.clf()
#    fig.seek(0)
#    return send_file(fig, mimetype="image/png")
