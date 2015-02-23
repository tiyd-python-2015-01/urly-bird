from flask import Flask
from hashids import Hashids
from .extensions import (
    db,
    migrate,
    debug_toolbar,
    bcrypt,
    login_manager
)

SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/urly_bird.db"
DEBUG = True
SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.from_object(__name__)

db.init_app(app)
debug_toolbar.init_app(app)
migrate.init_app(app, db)
bcrypt.init_app(app)
login_manager.init_app(app)
shortner = Hashids(salt='my name is url', min_length=4)

from . import views, models
