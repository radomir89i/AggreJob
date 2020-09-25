import os
import yaml

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    CONFIG_FOLDER = os.path.join(basedir, 'config')
    VACANCY_FOLDER = os.path.join(basedir, 'vacancy_data')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'moscow-never-sleeps'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    with open(os.path.join(CONFIG_FOLDER, 'db_credentials.yaml')) as f:
        PG_CREDENTIALS = yaml.load(f)

        login = PG_CREDENTIALS['login']
        password = PG_CREDENTIALS['password']
        host = PG_CREDENTIALS['host']
        port = PG_CREDENTIALS['port']
        db = PG_CREDENTIALS['db']

    SQLALCHEMY_DATABASE_URI = f'postgresql://{host}:{port}@{login}:{password}/{db}'



