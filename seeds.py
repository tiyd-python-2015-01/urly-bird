import csv
from hashids import Hashids
from faker import Factory
from random import randint
from urly_bird.app import db, models
import datetime

def seed_all(db):
    seed_users(db)
    seed_urls(db)


def seed_users(db):
    users_added = 0
    users_updated = 0
    with open('seed_users.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            user = models.User.query.filter_by(email=row['email']).first()
            if user is None:
                user = models.User()
                users_added += 1
            else:
                users_updated += 1
            for key, value in row.items():
                setattr(user, key, value)
            db.session.add(user)
        db.session.commit()


def seed_urls(db):
    urls_added = 0
    urls_updated = 0
    with open('seed_urls.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            url = models.URL.query.filter_by(long_address=row['long_address']).first()
            if url is None:
                url = models.URL()
                urls_added += 1
            else:
                urls_updated += 1
            for key, value in row.items():
                setattr(url, key, value)
            db.session.add(url)
            hashed_url = models.URL.query.filter_by(long_address=url.long_address).first()
            salt = "seasalt{}".format(hashed_url.id)
            hashed_id = Hashids(salt=salt, min_length=4).encode(hashed_url.id)
            hashed_url.short_address = hashed_id
        db.session.commit()


def seed_timestamps(db):
    #  create list of timestamps and ip_addresses and assign them to url_ids
    #  Then add them to the Timestamp table.
    fake = Factory.create()
    urls = models.URL.query.all()
    url_count = len(urls)-1
    for n in range(100000):
        fake_id = urls[randint(0, url_count)].id
        fake_user = fake.user_agent()
        fake_ip = fake.ipv4()
        fake_time = fake.date_time_between(datetime.date(2014, 1, 1))
        timestamp = models.Timestamp(url_id=fake_id,
                                     timestamp=fake_time,
                                     ip_address=fake_ip,
                                     user_agent=fake_user)
        db.session.add(timestamp)
    db.session.commit()
