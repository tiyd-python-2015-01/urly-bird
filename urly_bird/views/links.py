from flask import (Blueprint, render_template, flash, redirect, request,
                   url_for, session, send_file)
from flask.ext.login import login_required, current_user
from datetime import datetime
from pickle import dumps
from io import BytesIO
import matplotlib.pyplot as plt
from ..forms import LinkForm
from ..models import Link, Click
from ..extensions import db, shortner, flash_errors


links = Blueprint("links", __name__)


@links.route("/")
def index():
    if current_user.is_authenticated():
        return redirect(url_for("links.display_user_links", page=1))
    else:
        return redirect(url_for("links.show_all"))


@links.route("/user/<int:page>")
def display_user_links(page):
    all_links = Link.query.filter_by(owner=current_user.id).order_by(
        Link.id.desc()).paginate(page, per_page=20, error_out=False)
    return render_template("index.html", links=all_links)


@links.route("/add", methods=["GET", "POST"])
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
        return redirect(url_for("links.index"))
    else:
        flash_errors(form)
        return render_template("add_link.html", form=form)


@links.route("/link_data/<int:link_id>")
@login_required
def link_data(link_id):
    link = Link.query.get_or_404(link_id)
    return render_template("link_data.html", link=link)


@links.route("/<short>")
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
        return redirect(url_for("links.index"))


@links.route("/show_all")
def show_all():
    return redirect(url_for("links.show_page", page=1))


@links.route("/show_all/<int:page>")
def show_page(page):
    all_links = Link.query.order_by(Link.id.desc()).paginate(page,
                                    per_page=40, error_out=False)
    return render_template("show_all.html", links=all_links)


@links.route("/delete/<int:link_id>")
@login_required
def delete_item(link_id):
    record = Link.query.get(link_id)
    db.session.delete(record)
    db.session.commit()
    return redirect(url_for("links.index"))


@links.route("/edit_link/<int:link_id>", methods=["GET", "POST"])
@login_required
def edit_link(link_id):
    record = Link.query.get(link_id)
    form = LinkForm(obj=record)
    if form.validate_on_submit():
        form.populate_obj(record)
        db.session.commit()
        return redirect(url_for("links.index"))
    else:
        return render_template("edit_link.html", form=form,
                               post_url=url_for("links.edit_link",
                                                link_id=link_id))


def make_chart(link):
    data = link.clicks_by_day()
    dates = [item[0] for item in data]
    date_labels = [date.strftime("%b %d") if i % 2 else ""
                   for i, date in enumerate(dates)]
    num_clicks = [item[1] for item in data]

    ax = plt.subplot(111)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

    plt.title("Link Clicks by Day")
    plt.plot_date(x=dates, y=num_clicks, fmt="-")
    plt.xticks(dates, date_labels, rotation=45, size="x-small")
    plt.tight_layout()


@links.route("/link_data<int:link_id>.png")
@login_required
def link_click_chart(link_id):
    link = Link.query.get_or_404(link_id)
    make_chart(link)

    fig = BytesIO()
    plt.savefig(fig)
    plt.clf()
    fig.seek(0)
    return send_file(fig, mimetype="image/png")
