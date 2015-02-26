from datetime import datetime
import random
from flask import Blueprint, request, render_template, redirect, flash, url_for, send_file
from flask.ext.login import current_user, login_required
from hashids import Hashids

from urly_bird.forms import URLForm
from urly_bird.models import URL, Timestamp

from ..extensions import db
from urly_bird.stats import create_plot

urls = Blueprint("urls", __name__)


@urls.route("/")
def index():
    if not current_user.is_authenticated():
        urls = URL.query.order_by("id").all()
        return render_template("index.html", urls=reversed(urls[-5::]), domain=request.url_root)
    return redirect(url_for("urls.sites"))


@urls.route("/sites", methods=['GET', 'POST'])
@login_required
def sites():
    url_list = URL.query.filter_by(owner=current_user.id)
    form = URLForm()
    #edit_address(form.address)
    if form.validate_on_submit():
        url = URL.query.filter_by(long_address=form.address.data).first()
        if url:
            flash("You've already made a bookmark for this url.")
        else:
            url = URL(name=form.title.data,
                      description=form.description.data,
                      long_address=form.address.data,
                      owner=current_user.id,
                      clicks=0)
            db.session.add(url)
            # Once the url is added, we have its unique, numerical id.
            # Encode that id so that it becomes a short string and append it to the url.
            # Also check for redundant hashes so that we can match short addresses to users
            # Set the short_address attribute and commit.
            hashed_url = URL.query.filter_by(long_address=form.address.data).first()
            salt = "seasalt{}".format(current_user.id)
            hashed_id = Hashids(salt=salt, min_length=4).encode(hashed_url.id)
            while len(URL.query.filter_by(short_address=hashed_id).all()) > 0:
                salt = "seasalt{}".format(random.randint())
                hashed_id = Hashids(salt=salt, min_length=4).encode(hashed_url.id)
            hashed_url.short_address = hashed_id
            db.session.commit()
            flash("URL added!")
            return redirect(url_for("urls.index"))
    elif request.method == 'POST':
        flash("Error adding URL.")
    return render_template("user.html", form=form, urls=url_list, domain=request.url_root)


@urls.route('/b/<shorty>')
def route(shorty):
    url = URL.query.filter_by(short_address=shorty).first()
    timestamp = Timestamp(url_id=url.id,
                          timestamp=datetime.utcnow(),
                          ip_address=request.remote_addr,
                          user_agent=request.headers.get('User-Agent'))
    db.session.add(timestamp)
    db.session.commit()
    return redirect(url.long_address)

@urls.route('/e/<shorty>', methods=['GET', 'POST'])
@login_required
def edit(shorty):
    print("Edit")
    url = URL.query.filter_by(short_address=shorty).first()
    form = URLForm(title=url.name, description=url.description, address=url.long_address)
    if url and url.owner == current_user.id:
        if request.method == 'GET':
            return render_template("link.html", url=url, form=form, domain=request.url_root)
        elif request.method == 'POST':
            url.name = form.title.data
            url.long_address = form.address.data
            url.description = form.description.data
            db.session.commit()
            flash("Saved!")
    # Anything that fails the above if statements falls through to return index.html
    return redirect(url_for("urls.index"))

@urls.route('/s/<shorty>')
def stats(shorty):
    url = URL.query.filter_by(short_address=shorty).first_or_404()
    fig = create_plot(url.id)
    return send_file(fig, mimetype="image/png")



@urls.route('/d/<shorty>')
def delete(shorty):
    url = URL.query.filter_by(short_address=shorty).first()
    if url:
        db.session.delete(url)
        db.session.commit()
    return redirect(url_for("urls.index"))


def edit_address(address):
    if address.data and not re.match(r'^(http://)', address.data):
        address.data = "http://{}".format(address.data)
