from flask import Flask, render_template

from .extensions import (
   db,
   migrate,
   debug_toolbar,
   bcrypt,
   login_manager,
)

SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/urly-bird.db"
DEBUG = True
SECRET_KEY = 'development-key'

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(__name__)
app.config.from_pyfile('application.cfg', silent=True)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
db.init_app(app)
debug_toolbar.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app)

from . import views
