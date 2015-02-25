#!/usr/bin/env python

import os
import csv
from flask.ext.script import Manager, Shell, Server
from flask.ext.migrate import MigrateCommand
from flask.ext.script.commands import ShowUrls, Clean
from urlybird import app, db, models


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


if __name__ == '__main__':
    manager.run()


@manager.command
def seed_users():
    """Seed the books with all books in seed_books.csv."""
    users_added = 0
    with open('seed_users.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            person = models.User()
            users_added += 1
            for key, value in row.items():
                setattr(person, key, value)
            db.session.add(person)
        db.session.commit()
        print("{} users added.".format(users_added))


@manager.command
def seed_links():
    """Seed the books with all books in seed_books.csv."""
    links_added = 0
    with open('seed_links.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            link = models.Link()
            links_added += 1
            for key, value in row.items():
                setattr(link, key, value)
            db.session.add(link)
        db.session.commit()
        print("{} links added.".format(links_added))


@manager.command
def seed_clicks():
    """Seed the books with all books in seed_books.csv."""
    clicks_added = 0
    with open('seed_clicks.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            click = models.Link()
            clicks_added += 1
            for key, value in row.items():
                setattr(link, key, value)
            db.session.add(click)
        db.session.commit()
        print("{} links added.".format(clicks_added))

if __name__ == '__main__':
    manager.run()