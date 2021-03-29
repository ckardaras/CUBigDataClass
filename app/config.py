import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'to_the_moon'

    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:Dev12345!@localhost:5432/tothemoon"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
