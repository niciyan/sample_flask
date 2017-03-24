import os


class Config(object):
    SECRET_KEY = "dev key"
    SQLALCHEMY_DATABASE_URI = os.environ.get('mysqldriver')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True


config = {
        'development': DevelopmentConfig
        'default' : DevelopmentConfig
}
