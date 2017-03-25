from flask import Flask, render_template, request, redirect, url_for, flash
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from datetime import datetime
from flask_bootstrap import Bootstrap
from livereload import Server
import os
import logging
from logging import FileHandler, Formatter
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('mysqldriver')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SECRET_KEY'] = "development key"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
manager = Manager(app)
bootstrap = Bootstrap(app)

# logging.basicConfig(level='DEBUG', filename="sample.log")
file_handler = FileHandler('sample.log')
file_handler.setFormatter(Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
))
app.logger.addHandler(file_handler)

class NameForm(FlaskForm):
    text = StringField("your message", validators=[ Required() ])
    submit = SubmitField('送信')

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True, index=True)
    message = db.Column(db.String(64))
    date = db.Column(db.DateTime)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

@app.route('/')
def index():
    return render_template('index.html', messages=Message().query.order_by(Message.date.desc()).limit(6).all())

@app.route('/new', methods=['GET', 'POST'])
def new():
    form = NameForm() 
    # if request.method == 'POST':
    if form.validate_on_submit():
        # form.text.data
        now = datetime.now()
        me = Message(message=form.text.data, date=now)
        db.session.add(me)
        db.session.commit()
        flash('新しいメッセージを追加しました!!')
        app.logger.debug('new data inserted.')
        return redirect('/')
        print('passed')
    else:
        return render_template('new.html', form=form)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    # app.run()
    manager.run()
    # server = Server(app.wsgi_app)
    # server.serve()

