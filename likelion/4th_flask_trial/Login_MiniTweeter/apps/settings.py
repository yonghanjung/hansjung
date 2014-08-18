"""
settings.py

Configuration for Flask app

"""


class Config(object):
    # Set secret key to use session
    SECRET_KEY = "hanstobegreat"
    debug = False


class Production(Config):
    debug = True
    CSRF_ENABLED = False
    ADMIN = "icu.20071102@gmail.com"
    SQLALCHEMY_DATABASE_URI = 'mysql+gaerdbms:///blog?instance=hanstobegreat:myhans-data'
    migration_directory = 'migrations'
