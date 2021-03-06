import os
import pprint

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell

from app import create_app, db, search
from app.models import User, Message, Comment

app = create_app(os.getenv('flask_config') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, search=search, User=User, Message=Message)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def deploy():
    pprint.pprint(app.config)
    db.drop_all()
    db.create_all()
    User.generate_test_user()
    User.generate_fake()
    Message.generate_fake()
    Comment.generate_comments()
    search.create_index()


@manager.command
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def rundebug():
    pprint.pprint(app.url_map)
    pprint.pprint(app.config)
    app.config['SQLALCHEMY_ECHO'] = True
    app.run(use_reloader=False)


if __name__ == '__main__':
    manager.run()
