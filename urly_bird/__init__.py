from flask import Flask
import os
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')


from .extensions import (
    db,
    migrate,
    debug_toolbar,
    bcrypt,
    login_manager,
    config
)

SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/urly_bird.db"
DEBUG = True
SECRET_KEY = 'development-key'

app = Flask("URLybird", template_folder=tmpl_dir)
app.config.from_object(__name__)
app.config.from_pyfile('application.cfg', silent=True)

config.init_app(app)
db.init_app(app)
#debug_toolbar.init_app(app)
migrate.init_app(app, db)
bcrypt.init_app(app)
login_manager.init_app(app)

from . import views, models