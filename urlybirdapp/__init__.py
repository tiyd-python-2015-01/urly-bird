from flask import Flask

from .extensions import db, migrate, bcrypt, login_manager

SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/urlybird.db"
DEBUG = True
SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.from_object(__name__)

db.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app)
bcrypt.init_app(app)

from . import views, models
