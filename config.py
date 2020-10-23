import os
basedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'databases')


class Config(object):
    # main config
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    BCRYPT_LOG_ROUNDS = 12

    # mail settings
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'username'
    MAIL_PASSWORD = 'password'
    SECURITY_PASSWORD_SALT = 'email-confirm-key'

    # mail accounts
    ADMINS = ['username']
    MAIL_DEFAULT_SENDER = 'username'

    # languages
    LANGUAGES = {'it': 'Italian', 'en': 'English'}


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
