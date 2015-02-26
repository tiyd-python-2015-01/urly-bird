from flask import render_template, flash, redirect, request, url_for, session
from flask.ext.login import (login_user, login_required, logout_user,
                             current_user)
from datetime import datetime
from pickle import dumps
import matplotlib.pyplot as plt
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
        return redirect(url_for("display_user_links", page=1))
    else:
        return redirect(url_for("show_all"))


@app.route("/user/<int:page>")
def display_user_links(page):
    all_links = Link.query.filter_by(owner=current_user.id).order_by(
        Link.id.desc()).paginate(page, per_page=20, error_out=False)
    return render_template("index.html", links=all_links)


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
        db.session.commit()
        flash("Link successfully added!")
        return redirect(url_for("index"))
    else:
        flash_errors(form)
        return render_template("add_link.html", form=form)


@app.route("/link_data/<int:link_id>")
@login_required
def link_data(link_id):
    link = Link.query.get_or_404(link_id)
    return render_template("link_data.html", link=link)


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
                          user=current_user.id,
                          ip=request.environ['REMOTE_ADDR'],
                          user_agent=dumps(request.headers.get('User-Agent')))
            db.session.add(click)
            db.session.commit()
        else:
            click = Click(link=url.id,
                          date=datetime.utcnow(),
                          user=-1,
                          ip = request.environ['REMOTE_ADDR'],
                          user_agent=dumps(request.headers.get('User-Agent')))
            db.session.add(click)
            db.session.commit()
        url = url.original
        return redirect(url)
    else:
        flash("URL Not Found.")
        return redirect(url_for("index"))


@app.route("/show_all")
def show_all():
    return redirect(url_for("show_page", page=1))


@app.route("/show_all/<int:page>")
def show_page(page):
    all_links = Link.query.order_by(Link.id.desc()).paginate(page,
                                    per_page=40, error_out=False)
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


def make_chart(link):
    data = link.clicks_by_day()
    dates = [item[0] for item in data]
    date_labels = [date.strftime("%b %d") if i % 2 else ""
                   for i, date in enumerate(dates)]
    num_clicks = [item[1] for item in data]

    ax = plt.subplot()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

    plt.title("Link Clicks by Day")
    plt.plot_date(x=dates, y=num_clicks, fmt="-")
    plt.xticks(dates, date_labels, rotation=45, size="x-small")
    plt.tight_layout()


@app.route("/link_data<int:link_id>.png")
@login_required
def link_click_chart(link_id):
    link = Link.query.get_or_404(link_id)
    make_chart(link)

    fig = BytesIO()
    plt.savefig(fig)
    plt.clf()
    fig.seek(0)
    return send_file(fig, mimetype="image/png")
