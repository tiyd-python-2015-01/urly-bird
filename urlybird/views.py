from flask import render_template, redirect, request, url_for

from . import app, db


@app.route('/')
def index():
    return render_template('index.html')
