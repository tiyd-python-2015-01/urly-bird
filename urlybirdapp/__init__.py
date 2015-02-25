from flask import Flask

from .extensions import db, migrate, bcrypt, login_manager, config

SQLALCHEMY_DATABASE_URI = "postgres://localhost/urlybirddb"
DEBUG = True
SECRET_KEY = 'development key'

app = Flask("Urlybird: The Appening")
app.config.from_object(__name__)

config.init_app(app)
db.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app)
bcrypt.init_app(app)

from . import views, models
