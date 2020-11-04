import os

import yaml
from google.oauth2 import service_account


BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config:

    @staticmethod
    def get_creds(creds: str):
        with open(Config.CREDENTIALS_FILE) as f:
            config = yaml.safe_load(f)
        return config[creds]

    CONFIG_FOLDER = os.path.join(BASEDIR, 'config')
    EXPORT_FOLDER = os.path.join(BASEDIR, 'data_files')
    CREDENTIALS_FILE = os.path.join(CONFIG_FOLDER, 'credentials.yml')
    SECRET_KEY = os.environ.get('SECRET_KEY') or get_creds('secret_key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{password}@{host}:{port}/{db}'.format(**get_creds('db_credentials'))
    KEY_SKILLS_FILE = os.path.join(CONFIG_FOLDER, 'spec_key_skills.yml')


class GoogleDrive:
    SERVICE_ACCOUNT_FILE = os.path.join(Config.CONFIG_FOLDER, 'gdrive_credentials.json')
    SCOPES = ['https://www.googleapis.com/auth/drive']
    FOLDER_ID = '1HrUEphX1chXTYCr7k2DsX6Q8viDxd2as'
    GD_CREDENTIALS = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
