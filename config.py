import os


class Config(object):
    SECRET_KEY = "dev key"
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
    SQLALCHEMY_DATABASE_URI = os.environ.get('mysqldriver') or 'sqlite:///db.sqlite'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True


config = {
        'development': DevelopmentConfig,
        'default' : DevelopmentConfig
}
