# -*- coding: utf-8 -*-
from logging import StreamHandler, Formatter
from datetime import datetime

from flask import Flask, request
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_moment import Moment
from flask_msearch import Search
from flask_pagedown import PageDown
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis

from config import config

bootstrap = Bootstrap()
db = SQLAlchemy()
moment = Moment()
pagedown = PageDown()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
login_manager.login_message = 'このページにアクセスするには、ログインしてください。'
login_manager.login_message_category = 'warning'
search = Search()
redis_client = FlaskRedis()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)
    search.init_app(app)
    redis_client.init_app(app)

    @app.before_request
    def printer():
        now = datetime.now()
        redis_client.hincrby("access:"+now.strftime("%Y%m%d"), request.path, 1)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    # log configs(tempolary)
    syserr_handler = StreamHandler()
    syserr_handler.setFormatter(Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    ))
    app.logger.addHandler(syserr_handler)

    return app
