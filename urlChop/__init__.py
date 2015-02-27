from flask import Flask

from .extensions import (
    db,
    migrate,
    debug_toolbar,
    bcrypt,
    login_manager,
    bootstrap,
    config
)

SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/urlchop.db"
DEBUG = True
SECRET_KEY = 'SUPERDUPERSECRET'

app = Flask("urlChop")
app.config.from_object(__name__)
#app.config.from_pyfile('application.cfg', silent=True)

config.init_app(app)#this has to be the first one
db.init_app(app)
debug_toolbar.init_app(app)
migrate.init_app(app, db)
bcrypt.init_app(app)
login_manager.init_app(app)
bootstrap.init_app(app)

from . import views, models
#this import needs to be here because the Flask App itself needs to be
