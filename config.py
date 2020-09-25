import os
import yaml

basedir = os.path.abspath(os.path.dirname(__file__))
POSTGRES = yaml.safe_load(open('config/db_credentials.yml'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'moscow-never-sleeps'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
