from flask import render_template, flash, redirect, request, url_for, send_file, Blueprint
from flask.ext.login import login_user, login_required, logout_user, current_user
from datetime import datetime
from sqlalchemy import desc, func
import matplotlib.pyplot as plt
from io import BytesIO

from ..extensions import db
from ..forms import URLForm, editURL
from ..models import Link, Click

link_blueprint = Blueprint('link_blueprint', __name__, template_folder='templates')

def flash_errors(form, category="warning"):
    '''Flash all errors for a form.'''
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}".format(getattr(form, field).label.text, error), category)


@link_blueprint.route("/")
def index():
    return render_template('layout.html')

@link_blueprint.route("/your_links")
def your_links():
    links = current_user.links.order_by(desc(Link.date)).all()

    return render_template('showAll.html', links=links)

@link_blueprint.route('/shorten', methods=['GET', 'POST'])
@login_required
def shorten():
    form = URLForm()
    if request.method == 'POST':
        url_input = form.url.data
        link = Link(original_link = url_input)
        link.description = form.description.data
        link.date = datetime.now()
        link.user = current_user
        db.session.add(link)
        db.session.commit()
        link.get_short_link()
        db.session.commit()
        return render_template("shorten.html", short_link=link.short_link, form=form)
    return render_template("shorten.html", form=form)

@link_blueprint.route('/<hashid>')
@login_required
def short_link(hashid):
    link = Link.query.filter(Link.short_link == hashid).first()
    if link:
        click = Click(user_id=current_user.id,
                      link_id=link.id,
                      date = datetime.now())
        db.session.add(click)
        db.session.commit()
        return redirect(link.original_link)
    else:
        flash("Couldn't find link!")
        return redirect(url_for('link_blueprint.index'))

@link_blueprint.route('/show_all')
@login_required
def show_all():
    links = Link.query.order_by(desc(Link.date)).all()

    return render_template('showAll.html', links=links)

@link_blueprint.route('/link/<int:id>', methods=["GET", "POST"])
@login_required
def edit_link(id):
    link = Link.query.get(id)
    form = editURL(obj=link)
    if request.method == 'POST':
        form.populate_obj(link)
        link.description = form.description.data
        link.original_link = form.original_link.data
        db.session.add(link)
        db.session.commit()
        flash("URLybird updated your link")
        return redirect(url_for("link_blueprint.your_links"))
    return render_template("editLink.html",
                           form=form,
                           post_url=url_for("link_blueprint.edit_link", id=link.id),
                           short_link=link.short_link, link=link)

@link_blueprint.route("/delete/<int:id>", methods=['GET', 'POST'])
@login_required
def delete(id):
    link = Link.query.get(id)
    db.session.delete(link)
    db.session.commit()
    flash("Link has been deleted")
    return redirect(url_for("link_blueprint.your_links"))

@link_blueprint.route("/clicks")
@login_required
def get_clicks():
    user = current_user.id
    link_list = []
    clicks = Click.query.filter(Click.user_id == user).all()
    for click in clicks:
        link = Link.query.filter(Link.id == click.id).first()
        link_list.append(link)
    return render_template('clicks.html', clicks=clicks)

# @link_blueprint.route("/link/<int:id>/data")
# def click_data(id):
#     link = Link.query.get_or_404(id)
#     link_clicks_chart(id)
#     fig = BytesIO()
#     plt.savefig(fig)
#     fig.seek(0)
#     return send_file(fig, mimetype="image/png")
#
#
# @link_blueprint.route("/link/<int:id>_clicks.png")
# def link_clicks_chart(id):
#     link = Link.query.get_or_404(id)
#     data = link.clicks_by_day
#     dates = [c[1] for c in data]
#     num_clicks = [c[0] for c in data]
#     fig = BytesIO()
#     plt.plot_date(x=dates, y=num_clicks, fmt="-")
#     plt.savefig(fig)
#     fig.seek(0)
#     return send_file(fig, mimetype="image/png")

@link_blueprint.route("/link/<int:id>/data")
def make_clicks_chart(link):
    print(link.id)
    click_data = link.clicks_by_day
    dates = [c[0] for c in click_data]
    # every_other_date_label = [d if i % 2 else "" for i, d in enumerate(date_labels)]
    num_clicks = [c[1] for c in click_data]

    # ax = plt.subplot(111)
    # ax.spines["top"].set_visible(False)
    # ax.spines["right"].set_visible(False)
    # ax.get_xaxis().tick_bottom()
    # ax.get_yaxis().tick_left()

    plt.title("Clicks by day")
    plt.plot_date(x=num_clicks, y=dates, fmt="-")
    # plt.xticks(dates, every_other_date_label, rotation=45, size="x-small")
    plt.tight_layout()


@link_blueprint.route("/link/<int:id>_clicks.png")
def link_clicks_chart(id):
    print("link_clicks_chart {}".format(id))
    link = Link.query.get_or_404(id)
    make_clicks_chart(link)

    fig = BytesIO()
    plt.savefig(fig)
    plt.clf()
    fig.seek(0)
    return send_file(fig, mimetype="image/png")




