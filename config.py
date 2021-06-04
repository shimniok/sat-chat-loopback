import os
from datetime import timedelta
basedir = os.path.abspath(os.path.dirname(__file__))

def create_config():
    return Config()


class Config(object):
    DEVELOPMENT = False
    DEBUG = True
    TESTING = True
    CSRF_ENABLED = True
    SECRET_KEY = os.environ['SECRET_KEY']
    REMEMBER_COOKIE_DURATION = timedelta(seconds=300)
    REMEMBER_COOKIE_SECURE = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_REFRESH_EACH_REQUEST = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
