from faker import Factory
from urly_data.models import User, Links, Clicks
import random

links = Links.query.all()
max_time = int(datetime.now().timestamp)
min_time = max_time - (30*24*60*60)
for link in links:
    for _ in range(random.randint(100,500)):
        r_user = random.randint(1,5)
        r_when= datetime.fromtimestamp(random.randint(min_time,max_time))
        r_ip = fake.ipv4()
        r_agent = fake.user_agent()
        click = Clicks(r_user, link, r_when, r_ip, r_agent)
        db.session.add(click)
db.session.commit()
