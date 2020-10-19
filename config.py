import os

import yaml
from google.oauth2 import service_account


BASEDIR = os.path.abspath(os.path.dirname(__file__))
credentials_file = os.path.join(BASEDIR, 'config', 'credentials.yml')
KEY_SKILLS_FILE = os.path.join('config', 'spec_key_skills.yml')


def get_creds(creds: str):
    with open(credentials_file) as f:
        config = yaml.safe_load(f)
    return config[creds]


DB_CREDENTIALS = get_creds('db_credentials')
DB_CONN = 'postgresql://{user}:{password}@{host}:{port}/{db}'.format(**DB_CREDENTIALS)
EXPORT_FOLDER = os.path.join(BASEDIR, 'data_files')


class Config(object):
    CONFIG_FOLDER = os.path.join(BASEDIR, 'config')
    VACANCY_FOLDER = os.path.join(BASEDIR, 'vacancy_data')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'moscow-never-sleeps'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')


class GoogleDrive(object):
    SERVICE_ACCOUNT_FILE = os.path.join(BASEDIR, 'config', 'gdrive_credentials.json')
    SCOPES = ['https://www.googleapis.com/auth/drive']
    FOLDER_ID = '1HrUEphX1chXTYCr7k2DsX6Q8viDxd2as'
    GD_CREDENTIALS = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

