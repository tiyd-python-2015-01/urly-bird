#!/usr/bin/env python
import os
import csv
import random

from faker import Factory
from datetime import datetime

from flask.ext.script import Manager, Shell, Server
from flask.ext.migrate import MigrateCommand
from flask.ext.script.commands import ShowUrls, Clean

from urly_bird import create_app, db, models

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
    return dict(app=app,
                db=db,
                Link=models.Links,
                User=models.User,
                Clicks=models.Clicks)


@manager.command
def test():
    """Run the tests."""
    import pytest
    exit_code = pytest.main([TEST_PATH, '--verbose'])
    return exit_code

@manager.command
def seed():
    """Seed the links with all links in seed_links.csv."""
    with open('links.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        counter = 0
        for row in reader:
            link = models.Links(row['long'], row['title'],row['description'])
            link.set_short(counter)
            link.user = 1
            db.session.add(link)
            counter += 1
        db.session.commit()

@manager.command
def seed_clicks():
    fake = Factory.create()
    links = models.Links.query.order_by(models.Links.id.desc()).all()
    max_time = int(datetime.now().timestamp())
    min_time = max_time - (30*24*60*60)
    for link in links:
        for _ in range(random.randint(100,500)):
            r_user = random.randint(1,5)
            r_when= datetime.fromtimestamp(random.randint(min_time,max_time))
            r_ip = fake.ipv4()
            r_agent = fake.user_agent()
            click = models.Clicks(user_id=r_user,
                                  link_id=link.id,
                                  when= r_when,
                                  IP=r_ip,
                                  agent=r_agent)
            db.session.add(click)
        db.session.commit()


if __name__ == '__main__':
    manager.run()
