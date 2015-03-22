from faker import Factory
fake = Factory.create()


@manager.command
def make_clicks(n):
    for _ in range(1,n):
        click_time = fake.date_time_this_month()
        click = Click(bookmark_id = random.randint(1,17),
                      click_date = click_time,
                      user = random.randint(1,3),
                      ip_address = fake.ipv4())
        db.session.add(click)
        db.session.commit()

if __name__ == "__main__":
