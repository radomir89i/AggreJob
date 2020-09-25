import os
import yaml

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    CONFIG_FOLDER = os.path.join(basedir, 'config')
    VACANCY_FOLDER = os.path.join(basedir, 'vacancy_data')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'moscow-never-sleeps'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
