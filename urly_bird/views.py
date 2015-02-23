from flask import render_template, flash, redirect, request, url_for, session
from flask.ext.login import (login_user, login_required, logout_user,
                             current_user)
from datetime import datetime
from . import app, db, shortner
from .forms import LoginForm, RegistrationForm, LinkForm
from .models import User, Link, Click


def flash_errors(form, category="warning"):
    """Show all errors from a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}".format(
                getattr(form, field).label.text, error), category)


@app.route("/")
def index():
    if current_user.is_authenticated():
        return render_template("index.html")
    else:
        return redirect(url_for("show_all"))

@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    form = LinkForm()
    if form.validate_on_submit():
        submission = Link(original=form.original.data,
                          title=form.title.data,
                          description=form.description.data,
                          date=datetime.utcnow(),
                          owner=current_user.id)
        db.session.add(submission)
        db.session.flush()
        submission.short = shortner.encode(submission.id)
        print(submission.id, submission.short)
        db.session.commit()
        return render_template("success.html", shorturl=submission.short)
    else:
        flash_errors(form)
        return render_template("add_link.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("You were logged in!")
            return redirect(request.args.get("next") or url_for("index"))
        else:
            flash("E-mail address or password invalid.")
    flash_errors(form)
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/create_user", methods=["GET", "POST"])
def create_user():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash("E-mail address already in use.")
        else:
            user = User(name=form.name.data,
                        email=form.email.data,
                        password=form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            session["username"] = user.name
            flash("Registration Successful!  You have been logged in.")
            return redirect(url_for("index"))
    else:
        flash_errors(form)
    return render_template("register.html", form=form)


@app.route("/<short>")
def redirect_to(short):
    url = db.session.query(Link).filter_by(short=short).first()
    if url:
        if current_user.is_authenticated():
            click = Click(link=url.id,
                          date=datetime.utcnow(),
                          user=current_user.id)
            db.session.add(click)
            db.session.commit()
        else:
            click = Click(link=url.id,
                          date=datetime.utcnow(),
                          user=request.environ['REMOTE_ADDR'])
            db.session.add(click)
            db.session.commit()
        url = url.original
        return redirect(url)
    else:
        flash("URL Not Found.")
        return redirect(url_for("index"))


@app.route("/show_all")
def show_all():
    all_links = db.session.query(Link).order_by(Link.id.desc()).all()
    return render_template("show_all.html", links=all_links)


@app.route("/delete/<int:link_id>")
@login_required
def delete_item(link_id):
    record = Link.query.get(link_id)
    db.session.delete(record)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/edit_link/<int:link_id>", methods=["GET", "POST"])
@login_required
def edit_link(link_id):
    record = Link.query.get(link_id)
    form = LinkForm(obj=record)
    if form.validate_on_submit():
        form.populate_obj(record)
        db.session.commit()
        return redirect(url_for("index"))
    else:
        return render_template("edit_link.html", form=form,
                               post_url=url_for("edit_link", link_id=link_id))
