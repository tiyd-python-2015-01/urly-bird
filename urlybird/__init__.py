from flask import Flask

from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask.ext.bcrypt import Bcrypt
bcrypt = Bcrypt()

from flask.ext.login import LoginManager
login_manager = LoginManager()

from flask.ext.migrate import Migrate
migrate = Migrate()

from flask.ext.appconfig import HerokuConfig
config = HerokuConfig()


SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/urlybird.db"
DEBUG = True
SECRET_KEY = 'development-key'

app = Flask("urlybird")
app.config.from_object(__name__)

config.init_app(app)
db.init_app(app)
migrate.init_app(app, db)
bcrypt.init_app(app)
login_manager.init_app(app)


from . import views, models
