import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'to_the_moon'

    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:Dev12345!@54.165.83.41:5432/tothemoon"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SCHEDULER_API_ENABLED = True
