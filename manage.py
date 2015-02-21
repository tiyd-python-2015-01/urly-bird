from urlybird import app, db

from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script.commands import ShowUrls, Clean

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
manager.add_command("show-urls", ShowUrls())
manager.add_command("clean", Clean())


if __name__ == '__main__':
    manager.run()
