"""
settings.py

Configuration for Flask app

"""
from datetime import timedelta

class Config(object):
    # Set secret key to use session
    SECRET_KEY = "hanstobegreat"
    debug = False
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=2)


class Production(Config):
    debug = True
    CSRF_ENABLED = False
    ADMIN = "icu.20071102@gmail.com"
    SQLALCHEMY_DATABASE_URI = 'mysql+gaerdbms:///sessionpractice?instance=hanstobegreat:session0'
    migration_directory = 'migrations'