from flask import render_template, redirect, request, url_for
from .forms import UrlForm
from .models import LongUrl
from . import app, db
from hashids import Hashids


@app.route('/')
def index():
    new_url_form = UrlForm()
    return render_template('index.html', new_url_form=new_url_form)

@app.route('/add', methods=['POST'])
def add_url():
    hashids = Hashids()

    form = UrlForm()
    if form.validate_on_submit():
        url = LongUrl(form.text.data)
        short_url = hashids(form.text.data)
        db.session.add(url)
        db.session.commit()
    return redirect(url_for('index'))
