"""Extensions"""
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate
from flask.ext.debugtoolbar import DebugToolbarExtension
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
debug_toolbar = DebugToolbarExtension()
bcrypt = Bcrypt()
login_manager = LoginManager()
