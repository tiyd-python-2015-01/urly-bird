from flask import Flask

from .extensions import (
    db,
    migrate,
    debug_toolbar,
    bcrypt,
    login_manager,
    config
)

SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/urlybird.db"
DEBUG = True
SECRET_KEY = 'development-key'

app = Flask("URLyBird")
app.config.from_object(__name__)


config.init_app(app)
db.init_app(app)
debug_toolbar.init_app(app)
migrate.init_app(app, db)
bcrypt.init_app(app)
login_manager.init_app(app)

from . import views, models
