import json
import pprint
import os
from app import create_app, db
from app.models import User, Message
from flask_script import Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('flask_config') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, User=User, Message=Message)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def deploy():
    db.drop_all()
    db.create_all()
    User.generate_test_user()
    User.generate_fake()
    Message.generate_fake()


@manager.command
def rundebug():
    pprint.pprint( app.url_map )
    pprint.pprint( app.config )
    app.config['SQLALCHEMY_ECHO'] = True
    app.run(use_reloader=False)


if __name__ == '__main__':
    manager.run()
