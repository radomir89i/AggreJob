import os
import json

import yaml
from google.oauth2 import service_account


basedir = os.path.abspath(os.path.dirname(__file__))
credentials_file = os.path.join(basedir, 'config', 'credentials.yml')


def get_creds(creds: str):
    with open(credentials_file) as f:
        config = yaml.safe_load(f)
    return config[creds]


SERVICE_ACCOUNT_FILE = os.path.join(basedir, 'config', 'gdrive_credentials.json')
SCOPES = ['https://www.googleapis.com/auth/drive']
GD_CREDENTIALS = service_account.Credentials.from_service_account_file(
              SERVICE_ACCOUNT_FILE, scopes=SCOPES)
DB_CREDENTIALS = get_creds('db_credentials')
EXPORT_FOLDER = os.path.join(basedir, 'data_files')
DB_CONN = 'postgresql://{user}:{password}@{host}:{port}/{db}'.format(**DB_CREDENTIALS)


class Config(object):
    CONFIG_FOLDER = os.path.join(basedir, 'config')
    VACANCY_FOLDER = os.path.join(basedir, 'vacancy_data')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'moscow-never-sleeps'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')


if __name__ == '__main__':
    print(get_creds('gdrive_credentials')['private_key'])
