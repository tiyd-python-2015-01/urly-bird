from flask import Flask, request, session, redirect, url_for, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

DATABASE = '/tmp/urly_bird.db'
DEBUG = True
SECRET_KEY = 'development-key'
SQLALCHEMY_DATABASE_URI = "sqlite:///" + DATABASE

app = Flask(__name__)
app.config.from_object(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

@app.route('/')
def index():
    return render_template('layout.html')

if __name__ == '__main__':
    manager.run()