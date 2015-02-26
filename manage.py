import csv
from datetime import datetime
from faker import Faker
from random import randint

from flask.ext.script import Manager, Shell, Server
from flask.ext.migrate import MigrateCommand
from flask.ext.script.commands import ShowUrls, Clean

from urly_bird import app, db, bcrypt, models, shortner

manager = Manager(app)
manager.add_command('server', Server())
manager.add_command('db', MigrateCommand)
manager.add_command('show-urls', ShowUrls())
manager.add_command('clean', Clean())


@manager.shell
def make_shell_context():
    return dict(app=app, db=db)


@manager.command
def seed_users():
    users_added = 0
    users_updated = 0

    with open('users.csv') as csvfile:
        csv_items = csv.DictReader(csvfile)
        for row in csv_items:
            user = models.User.query.filter_by(email=row['email']).first()
            if user is None:
                user = models.User()
                users_added += 1
            else:
                users_updated += 1
            for key, value in row.items():
                if key == 'password':
                    setattr(user, 'encrypted_password',
                            bcrypt.generate_password_hash(value))
                else:
                    setattr(user, key, value)
            db.session.add(user)
        db.session.commit()
    print("{} users added, {} users updated.".format(users_added,
                                                     users_updated))


@manager.command
def seed_links():
    links_added = 0
    fake = Faker()
    users = models.User.query.count()
    existing_links = models.Link.query.count()
    for x in range(existing_links+1, 1001):
        new_link = models.Link(original=fake.url(),
                               title=fake.catch_phrase(),
                               description=fake.text(),
                               date=fake.date_time_between(start_date='-1y',
                                                           end_date='now'),
                               owner=randint(1, users),
                               short=shortner.encode(x))
        db.session.add(new_link)
    db.session.commit()
    print("{} links added.".format(1000-existing_links))


@manager.command
def seed_clicks():
    clicks_added = 0
    links = models.Link.query.count()
    users = models.User.query.count()
    fake = Faker()
    for x in range(100000):
        index = randint(1, links)
        link = models.Link.query.get(index)
        new_click = models.Click(link=index,
                                 date=fake.date_time_between(
                                        start_date='{}d'.format(
                                        (link.date-datetime.utcnow()).days),
                                        end_date='now'),
                                        user=randint(1, users),
                                        ip=fake.ipv4(),
                                        user_agent=fake.user_agent())
        db.session.add(new_click)
    db.session.commit()
    print("Clicks seeded.")


if __name__ == '__main__':
    manager.run()
