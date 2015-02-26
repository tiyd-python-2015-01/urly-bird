from datetime import datetime
from ipwhois import IPWhois
from ipwhois.utils import get_countries
from io import BytesIO
import matplotlib.pyplot as plt
from bokeh.plotting import figure, output_file, show

"""Add your views here."""

from flask import Blueprint, render_template, flash, redirect, url_for, send_file
from flask.ext.login import login_required, current_user

from ..extensions import db
from ..forms import LinkAddForm, LinkUpdateForm
from ..models import Links, Clicks

linksb = Blueprint("linksb",__name__)


@linksb.route("/")
def index():
    if current_user.is_authenticated():
        links = Links.query.filter_by(user=current_user.id).order_by(Links.id.desc())
        return render_template("index.html",links=links)
    else:
        return render_template("index.html",links=[])


@linksb.route("/links/<int:id>")
@login_required
def links_user(id):
    links = Links.query.filter_by(user=id).order_by(Links.id.desc())
    return render_template("links.html",links=links)


@linksb.route("/all_links")
def all_links():
    links = Links.query.order_by(Links.id.desc()).all()
    return render_template("all_links.html",links=links)


@linksb.route("/add_link", methods=["GET", "POST"])
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
        return redirect(url_for("linksb.index"))
    return render_template("add_link.html", form=form)


@linksb.route("/delete_link/<int:id>", methods=["GET", "POST"])
def delete_link(id):
    link_id = id
    link = Links.query.get(link_id)
    db.session.delete(link)
    db.session.commit()
    links = Links.query.filter_by(user=current_user.id).order_by(Links.id.desc())
    return render_template("index.html",links=links)


@linksb.route('/update_link/<int:id>', methods=["GET", "POST"])
@login_required
def update_link(id):
    update_link = Links.query.get(id)
    form = LinkUpdateForm(obj=update_link)
    if form.validate_on_submit():
        form.populate_obj(update_link)
        db.session.commit()
        return redirect(url_for("linksb.index"))
    return render_template("update_link.html",
                            update_url = url_for("linksb.update_link",id=update_link.id),
                            form=form)


@linksb.route('/urly/<new_url>')
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


def get_country(ip):
    countries = get_countries()
    obj = IPWhois(ip)
    results = obj.lookup(False)
    return countries[results['nets'][0]['country']]


@linksb.route("/link_clicks/<int:id>")
def link_clicks(id):
    link = Links.query.get_or_404(id)
    country_data = link.clicks_by_country()

    #for ip,num_clicks in country_data:
    #    try:
    #       country = get_country(ip)
    #       flash(country)
    #       fin_list.append((country,num_clicks))
    #    except:
    #       pass
    sorted_list = sorted(country_data, key=lambda tup: tup[1], reverse=True)
    return render_template("link_data.html",
                           link=link, countries=sorted_list)



@linksb.route("/link_clicks/<int:id>_clicks.png")
def link_clicks_chart(id):
    link = Links.query.get_or_404(id)
    click_data = link.clicks_by_day()
    dates = [c[0] for c in click_data]
    date_labels = [d.strftime("%b %d") for d in dates]
    every_other_date_label = [d if i % 2 else "" for i, d in enumerate(date_labels)]
    num_clicks = [c[1] for c in click_data]
    ax = plt.subplot(111)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    plt.title("Clicks by day")
    fig = plt.gcf()
    fig.set_size_inches(6,4)
    plt.plot_date(x=dates, y=num_clicks, fmt="-")
    plt.xticks(dates, every_other_date_label, rotation=45, size="x-small")
    plt.tight_layout()

    fig = BytesIO()  # will store the plot as bytes
    plt.savefig(fig)
    plt.clf()
    fig.seek(0) #go back to the beginning
    return send_file(fig, mimetype="image/png")


@linksb.route("/stats")
def stats():
    links = Links.query.all()
    pairs=[]
    for link in links:
        data = link.clicks_by_day()
        tot = sum([c[1] for c in data])
        pairs.append((link,tot))
    sorted_list = sorted(pairs, key=lambda tup: tup[1], reverse=True)
    return render_template("stats.html",data=sorted_list)
