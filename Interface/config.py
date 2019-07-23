import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_ULR') or \
        'sqlite:///' + os.path.join(basedir, 'AnaEE.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
