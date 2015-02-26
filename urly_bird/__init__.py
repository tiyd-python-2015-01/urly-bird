from flask import Flask, Blueprint
from .views.user import user_blueprint
from .views.link import link_blueprint
from .views.api import api

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

def create_app():
    app = Flask("urly_bird")
    app.config.from_object(__name__)
    app.config.from_pyfile('application.cfg', silent=True)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(link_blueprint)
    app.register_blueprint(api, url_prefix='/api/v1')

    config.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    return app