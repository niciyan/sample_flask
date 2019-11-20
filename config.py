import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = "dev key"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///db.sqlite'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FLASKY_COMMENTS_PER_PAGE = 6
    FLASKY_POSTS_PER_PAGE = 8
    JSON_AS_ASCII = False
    # when backend is elasticsearch, MSEARCH_INDEX_NAME is unused
    # flask-msearch will use table name as elasticsearch index name unless set __msearch_index__
    MSEARCH_INDEX_NAME = 'msearch'
    # simple,whoosh,elaticsearch, default is simple
    MSEARCH_BACKEND = 'whoosh'
    # table's primary key if you don't like to use id, or set __msearch_primary_key__ for special model
    MSEARCH_PRIMARY_KEY = 'id'
    # auto create or update index
    MSEARCH_ENABLE = True
    REDIS_URL = "redis://:@localhost:6379/0"


    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class SqliteConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    PREFERRED_URL_SCHEME = "https"
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class HerokuConfig(ProductionConfig):
    pass


config = {
    'default': DevelopmentConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'sqlite': SqliteConfig,
    'production': ProductionConfig,
    'heroku': HerokuConfig
}
