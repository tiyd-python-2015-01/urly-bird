from flask import render_template, flash, redirect, request, url_for
from flask.ext.login import login_user, login_required, logout_user

from . import app, db
from .forms import LoginForm, RegistrationForm
from .models import User, Link, CreateLinkForm


@app.route("/")
def home():


@app.route("register")
def register():

@app.route("login")
def login():

@app.route("index")
def create_links:

@app.route("user/links")
def user_home():

@app.route("click_data")
def user_data():
