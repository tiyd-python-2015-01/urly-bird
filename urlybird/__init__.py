from flask import Flask

from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()

app = Flask(__name__)

from . import views, models
