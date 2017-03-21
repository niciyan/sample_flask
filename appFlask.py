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


app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('mysqldriver')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SECRET_KEY'] = "development key"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
manager = Manager(app)
bootstrap = Bootstrap(app)


class NameForm(FlaskForm):
    text = StringField("your message", validators=[ Required() ])
    submit = SubmitField('送信')

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True, index=True)
    message = db.Column(db.String(64))
    date = db.Column(db.DateTime)


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
        return redirect('/')
        print('passed')
    else:
        return render_template('new.html', form=form)


if __name__ == '__main__':
    manager.run()
    # server = Server(app.wsgi_app)
    # server.serve()

