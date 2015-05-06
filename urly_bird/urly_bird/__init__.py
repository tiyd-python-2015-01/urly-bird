from flask import Flask
from hashids import Hashids
from .extensions import (
    db,
    migrate,
    debug_toolbar,
    config,
    bcrypt,
    login_manager
)

SQLALCHEMY_DATABASE_URI = "postgres://localhost/urly_bird"
DEBUG = True
SECRET_KEY = 'development-key'


#def create_app():
app = Flask("urly_bird")
app.config.from_object(__name__)

config.init_app(app)
db.init_app(app)
debug_toolbar.init_app(app)
migrate.init_app(app, db)
bcrypt.init_app(app)
login_manager.init_app(app)

    #return app

hashid = Hashids(salt="salt mines dehydrate the world")

from . import models, views
