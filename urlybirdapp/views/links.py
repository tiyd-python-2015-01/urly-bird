import random
from flask import Blueprint, render_template, redirect, flash, url_for, request, send_file
from flask.ext.login import current_user
from sqlalchemy import desc
from ..forms import AddLink, EditLink
from ..models import Links, Click
from ..extensions import db
from datetime import datetime
from io import BytesIO
import matplotlib.pyplot as plt

links = Blueprint("links", __name__)


def flash_errors(form, category="warning"):
    '''Flash all errors for a form.'''
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}".format(getattr(form, field).label.text, error),
                                                                   category)

@links.route('/')
def index():
    link_list = Links.query.order_by(desc(Links.id)).all()
    return render_template('index.html', link_list=link_list)


@links.route('/addlink', methods=['GET', 'POST'])
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
            return redirect(url_for('users.home_view'))
    else:
        flash_errors(form)
        return render_template('addlink.html', form=form)


@links.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_bookmark(id):
    current = Links.query.get(id)
    form = EditLink(obj=current)
    if form.validate_on_submit():
        form.populate_obj(current)
        db.session.commit()
        flash('Bookmark Updated')
        return redirect(url_for('users.home_view'))
    else:
        flash_errors(form)
    return render_template('editlink.html', form=form,
                            update_url=url_for('links.edit_bookmark', id=current.id))


@links.route('/delete/<int:id>', methods=['GET'])
def delete_bookmark(id):
    current = Links.query.get(id)
    db.session.delete(current)
    db.session.commit()
    flash('Bookmark Deleted!!')
    return redirect(url_for('users.home_view'))


@links.route('/<int:id>/data')
def link_data(id):
    link = Links.query.get_or_404(id)
    return render_template('link_data.html', link=link)

@links.route('/link/<int:id>_clicks.png/')
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


@links.route('/b/<tag>')
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
