from flask import Flask, render_template
#from flask_wtf.csrf import CsrfProtect
from .extensions import (
   db,
   migrate,
   debug_toolbar,
   bcrypt,
   login_manager,
   config
)

SQLALCHEMY_DATABASE_URI = "postgres://localhost/urly_bird"
DEBUG = True
SECRET_KEY = 'development-key'

app = Flask("urly_bird")

app.config.from_object(__name__)
config.init_app(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
db.init_app(app)
debug_toolbar.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app)
login_manager.login_view = "login"

from . import views, models
