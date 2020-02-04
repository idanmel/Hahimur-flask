import os


class Config(object):
    SECRET_KEY = os.urandom(16)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
