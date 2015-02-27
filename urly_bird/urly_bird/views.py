from flask import render_template, flash, request, url_for, redirect, ext
from .forms import LoginForm, RegistrationForm
from . import app, db
from .utils import flash_errors
from .models import User, Link

"""Add your views here."""



@app.route("/logout", methods=["GET"])
@ext.login.login_required
def logout():
    ext.login.logout_user()
    return redirect("/login")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/index", methods=["POST"])
@ext.login.login_required
def index():
    return render_template("layout.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            ext.login.login_user(user)
            flash("Logged in successfully.")
            return redirect(request.args.get('next') or url_for("index"))
        else:
            flash("That email or password is not correct.")

    flash_errors(form)
    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.name.data).first()
        if user:
            flash("A user with that user name already exists.")
        else:
            user = User(name=form.name.data,
                        email=form.email.data,
                        password=form.password.data)
            db.session.add(user)
            db.session.commit()
            login(user)
            flash("You have been registered and logged in.")
            return redirect(url_for("index"))
    else:
        flash_errors(form)

    return render_template("register.html", form=form)
