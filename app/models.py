# -*- coding: utf-8 -*-
import hashlib
from datetime import datetime

import bleach
from flask import request
from flask_login import UserMixin
from markdown import markdown
from werkzeug.security import check_password_hash, generate_password_hash

from . import db
from . import login_manager


class Message(db.Model):
    __tablename__ = 'messages'
    __searchable__ = ['body']
    id = db.Column(db.Integer, primary_key=True, index=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow())
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref='message', lazy='dynamic')

    def to_json(self):
        post = {
            'id': self.id,
            'body': self.body_html,
            'timestamp': self.date
        }
        return post

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

    @staticmethod
    def generate_fake(count=10):
        from random import seed, randint, choice

        seed()
        user_count = User.query.count()
        SAMPLE_MESSAGES = [
            "# いいんじゃない？\nhi there",
            "> おｋ  \n> im good.",
            "## こんにちは\nhello",
            "_おつかれさん_",
            "**ただいま**",
            "# 会議中\ncall me later...",
            "### continueed\ndid not reach end",
            "Hello!",
            "`元気`  げんき",
        ]
        for i in range(count):
            u = User.query.offset(randint(0, user_count - 1)).first()
            m = Message(body=choice(SAMPLE_MESSAGES), date=datetime.utcnow(), author=u)
            db.session.add(m)

        db.session.commit()


db.event.listen(Message.body, 'set', Message.on_changed_body)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Message', backref='author', lazy='dynamic')
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow())
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow())
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    avatar_hash = db.Column(db.String(32))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(
                self.email.encode('utf-8')).hexdigest()

    def gravatar(self, size=100, default='identicon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = self.avatar_hash or hashlib.md5(
            self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)

    @staticmethod
    def generate_test_user():
        user = User(username='john', email='john@example.com', password='cat')
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            u = User(email=forgery_py.internet.email_address(),
                     username=forgery_py.internet.user_name(True),
                     password=forgery_py.lorem_ipsum.word(),
                     name=forgery_py.name.full_name(),
                     location=forgery_py.address.city(),
                     about_me=forgery_py.lorem_ipsum.sentence(),
                     member_since=forgery_py.date.date(True))
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

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

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    message_id = db.Column(db.Integer, db.ForeignKey('messages.id'))

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'code', 'em', 'i',
                        'strong']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

    @staticmethod
    def generate_comments(n=5):
        from random import seed, choice, randint
        seed()

        user_count = User.query.count()

        SAMPLE_COMMENTS = [
            'good post.',
            'this is bad.',
            'you are clever!',
            'NOT SHOWN.',
            'it sounds good.',
            'I am interested in this post.',
            'NICE ONE.',
            'You gave me a nice explanation.',
            'OMG!',
            'Hi, author.',
        ]

        messages = Message.query.all()
        for m in messages:
            for i in range(randint(0, n)):
                u = User.query.offset(randint(0, user_count - 1)).first()
                c = Comment(
                    body=choice(SAMPLE_COMMENTS),
                    author=u,
                    message=m
                )
                db.session.add(c)
        db.session.commit()


db.event.listen(Comment.body, 'set', Comment.on_changed_body)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
