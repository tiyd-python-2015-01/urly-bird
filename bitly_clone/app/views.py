from flask import render_template, flash, redirect, request, url_for
from flask.ext.login import login_user

from . import app, db
#from .forms import LoginForm, RegistrationForm
from .models import Book, User

@app.route("/")
def index():
    return render_template("index.html")
