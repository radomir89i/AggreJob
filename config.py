import os
import logging

import yaml
from google.oauth2 import service_account


BASEDIR = os.path.abspath(os.path.dirname(__file__))


def get_creds(creds: str, file: str):
    with open(file) as f:
        config = yaml.safe_load(f)
    return config[creds]


class Config:
    CONFIG_FOLDER = os.path.join(BASEDIR, 'config')
    EXPORT_FOLDER = os.path.join(BASEDIR, 'data_files')
    LOGS_FOLDER = os.path.join(BASEDIR, 'logs')
    CREDENTIALS_FILE = os.path.join(CONFIG_FOLDER, 'credentials.yml')
    SECRET_KEY = os.environ.get('SECRET_KEY') or get_creds('secret_key', CREDENTIALS_FILE)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{password}@{host}:{port}/{db}'.format(**get_creds('db_credentials', CREDENTIALS_FILE))
    PG_CONNECTION = 'host={host} dbname={db} user={user} password={password}'.format(**get_creds('db_credentials', CREDENTIALS_FILE))
    KEY_SKILLS_FILE = os.path.join(CONFIG_FOLDER, 'spec_key_skills.yml')
    SPECIALIZATIONS = ['python', 'java', 'c++']

    logging.basicConfig(format='%(levelname)s - %(asctime)s - %(message)s',
                        datefmt='%d - %b - %y %H:%M:%S',
                        filename=os.path.join(LOGS_FOLDER, 'log.log'),
                        level=logging.INFO)

class GoogleDrive:
    SERVICE_ACCOUNT_FILE = os.path.join(Config.CONFIG_FOLDER, 'gdrive_credentials.json')
    SCOPES = ['https://www.googleapis.com/auth/drive']
    FOLDER_ID = '1HrUEphX1chXTYCr7k2DsX6Q8viDxd2as'
    GD_CREDENTIALS = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
