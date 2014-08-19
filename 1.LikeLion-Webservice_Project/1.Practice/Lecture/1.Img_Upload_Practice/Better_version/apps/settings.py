import os

# from secret_keys import CSRF_SECRET_KEY, SESSION_KEY


class Config(object):
    # Set secret keys for CSRF protection
    # SECRET_KEY = CSRF_SECRET_KEY
    # CSRF_SESSION_KEY = SESSION_KEY
    debug = False


class Production(Config):
    DEBUG = True
    # CSRF_ENABLED = True
    ADMIN = "lla@lla.com"