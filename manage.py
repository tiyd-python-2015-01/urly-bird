#!/usr/bin/env python
import os
from flask.ext.script import Manager, Server, Shell
from flask.ext.migrate import MigrateCommand
from flask.ext.script.commands import ShowUrls, Clean

from urly_bird import create_app, db
import seeds


HERE = os.path.abspath(os.path.dirname(__file__))
TEST_PATH = os.path.join(HERE, 'tests')

app = create_app()
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
def seed_all():
    seeds.seed_all(db)
@manager.command
def seed_users():
    seeds.seed_users(db)
@manager.command
def seed_urls():
    seeds.seed_urls(db)
@manager.command
def seed_timestamps():
    seeds.seed_timestamps(db)

if __name__ == '__main__':
    manager.run()
