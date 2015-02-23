from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.debugtoolbar import DebugToolbarExtension
from flask.ext.migrate import Migrate


migrate = Migrate()
debug_toolbar = DebugToolbarExtension()
db = SQLAlchemy()
