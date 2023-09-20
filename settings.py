import os
from string import ascii_letters, digits


class Config(object):
    FLASK_APP = os.getenv('FLASK_APP', default='yacut')
    FLASK_ENV = os.getenv('FLASK_ENV', default='development')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', default='sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', default='supersecretkey')


ALLOWED_CHAR = ascii_letters + digits
MIN_USER_SHORT = 1
MAX_USER_SHORT = 16