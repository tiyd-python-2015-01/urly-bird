import os

from flask.ext.script import Manager, Shell, Server
from flask.ext.migrate import MigrateCommand
from flask.ext.script.commands import ShowUrls, Clean
from UrlyBird import app, db
from UrlyBird.models import Click
from faker import Factory
from random import randint
fake = Factory.create()

HERE = os.path.abspath(os.path.dirname(__file__))
TEST_PATH = os.path.join(HERE, 'tests')

manager = Manager(app)
manager.add_command('server', Server())
manager.add_command('db', MigrateCommand)
manager.add_command('show-urls', ShowUrls())
manager.add_command('clean', Clean())


@manager.shell
def make_shell_context():
    """ Creates a python REPL with several default imports
        in the context of the app
    """

    return dict(app=app, db=db)


@manager.command
def test():
    """Run the tests."""
    import pytest
    exit_code = pytest.main([TEST_PATH, '--verbose'])
    return exit_code



@manager.command
def make_clicks():
    for _ in range(1,10000 ):
        click_time = fake.date_time_this_month()
        click = Click(bookmark_id = randint(1,17),
                             click_date = click_time,
                             user_id = randint(1,3),
                             ip_address = fake.ipv4())
        db.session.add(click)
        db.session.commit()

if __name__ == '__main__':
    manager.run()
