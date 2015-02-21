from flask import Flask

from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/urlybird.db"
DEBUG = True
SECRET_KEY = 'development-key'

app = Flask(__name__)
app.config.from_object(__name__)

db.init_app(app)

from . import views, models
