from urlybird import app, db

from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script.commands import ShowUrls, Clean

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
manager.add_command("show-urls", ShowUrls())
manager.add_command("clean", Clean())

@manager.shell
def make_shell_context():
    """ Create a python REPL with several default imports
        in the context of the app.
    """
    return dict(app=app, db=db)



if __name__ == '__main__':
    manager.run()
