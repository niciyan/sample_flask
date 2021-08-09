import os
import pprint

from app import create_app, db, search
from app.models import User, Message, Comment, EnglishWord

app = create_app(os.getenv('flask_config') or 'default')


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, User=User, Message=Message, EnglishWord=EnglishWord)


@app.cli.command("deploy")
def deploy():
    pprint.pprint(app.config)
    db.drop_all()
    db.create_all()
    User.generate_test_user()
    User.generate_fake()
    Message.generate_fake()
    Comment.generate_comments()
    search.create_index()


@app.cli.command("test")
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@app.cli.command("debug")
def rundebug():
    pprint.pprint(app.url_map)
    pprint.pprint(app.config)
    app.config['SQLALCHEMY_ECHO'] = True
    app.run(use_reloader=False)


if __name__ == '__main__':
    app.run()
