from flask import Flask, render_template

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

app = Flask('urly_bird')
app.config.from_object(__name__)
app.config.from_pyfile('application.cfg', silent=True)
config.init_app(app)
db.init_app(app)
debug_toolbar.init_app(app)
migrate.init_app(app, db)
bcrypt.init_app(app)
login_manager.init_app(app)

from . import views, models
