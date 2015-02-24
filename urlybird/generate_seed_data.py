from faker import Factory
from .views import shorten_url
from .models import Bookmark, User, BookmarkUser, Click
import random
from urlybird.app import db


def create_user(user_id=1):
    fake = Factory.create()

    email = fake.email()
    name = fake.name()
    password = fake.password()
    if user_id == 0:
        user = User(id=0, email=email, name=name, password=password)
    else:
        user = User(email=email, name=name, password=password)
    print('user created: {}'.format(user))
    db.session.add(user)
    db.session.commit()


def create_bookmarks(num=30):
    fake = Factory.create()
    for _ in range(1, num+1):
        title = fake.company()
        description = fake.text(max_nb_chars=40)
        url = fake.url()
        bookmark = Bookmark(title=title,
                            description=description,
                            url=url,
                            short_url=shorten_url(url))
        db.session.add(bookmark)
    db.session.commit()

def user_to_bookmark(user_id, num=10):
    for counter in range(1, num+1):
        bookmark_user = BookmarkUser(user_id=user_id,
                                     item_id=random.randint(1,num))
        db.session.add(bookmark_user)
    db.session.commit()


def click_creation(user_count):
    fake=Factory.create()

    for num in range(0,user_count+1):
        for count in range(0,10):
            item_id = random.randint(1,30)
            timestamp = fake.date_time_between(start_date="-30d",
                                               end_date="now")
            click = Click(item_id = item_id,
                          user_id = num,
                          timestamp = timestamp,
                          user_ip_address = fake.ipv4(),
                          user_agent =fake.user_agent())
            db.session.add(click)
    db.session.commit()
    return user_count * 10
