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

SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/urly_bird.db"
DEBUG = True
SECRET_KEY = 'development-key'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_pyfile('application.cfg', silent=True)

config.init_app(app)
db.init_app(app)
debug_toolbar.init_app(app)
migrate.init_app(app, db)
bcrypt.init_app(app)
login_manager.init_app(app)

hashid = Hashids(salt=app.config['SECRET_KEY'])

from . import views, models
