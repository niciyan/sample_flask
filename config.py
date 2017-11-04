import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = "dev key"
    SQLALCHEMY_DATABASE_URI = os.environ.get('mysqldriver') or 'sqlite:///db.sqlite'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FLASKY_COMMENTS_PER_PAGE = 6
    FLASKY_POSTS_PER_PAGE = 8

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True

class SqliteConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') 

class HerokuConfig(ProductionConfig):
    pass


config = {
        'default' : DevelopmentConfig,
        'development': DevelopmentConfig,
        'sqlite': SqliteConfig,
        'production': ProductionConfig,
        'heroku': HerokuConfig
}
