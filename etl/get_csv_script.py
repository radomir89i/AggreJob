import io
import os

import pandas as pd
from sqlalchemy import create_engine

from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.discovery import build

from config import DB_CONN, EXPORT_FOLDER
from config import GoogleDrive


service = build('drive', 'v3', credentials=GoogleDrive.GD_CREDENTIALS)

result = service \
    .files() \
    .list(
        pageSize=1000,
        fields='nextPageToken, files(id, name, mimeType)') \
    .execute()['files']


def delete_csv_files() -> None:

    """
    Deletes all *.csv files in Google Drive folder.
    """

    for file in result:
        if file['mimeType'] == 'text/csv':
            service.files().delete(fileId=file['id']).execute()


def get_csv_files(target_folder=EXPORT_FOLDER) -> None:

    """
    Gets all *.csv files from Google Drive folder and puts them in target folder.
    :param target_folder: path to folder where downloaded files should be placed
    """

    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    for file in result:
        if file['mimeType'] == 'text/csv':
            request = service.files().get_media(fileId=file['id'])
            fh = io.FileIO(os.path.join(target_folder, file['name']), 'wb')
            downloader = MediaIoBaseDownload(fh, request)

            done = False
            while not done:
                status, done = downloader.next_chunk()
                print("Download %d%%." % int(status.progress() * 100))


def load_from_csv_to_database(target_folder=EXPORT_FOLDER) -> None:

    """
    Loads all *.csv files from target folder to database.
    :param target_folder: path to *csv files folder
    """

    engine = create_engine(DB_CONN)
    files = [os.path.join(target_folder, f) for f in os.listdir(target_folder) if f.endswith('.csv')]
    for file in files:
        data = pd.read_csv(file)
        data.to_sql('vacancy', engine, if_exists='append', index=False)


if __name__ == '__main__':
    # get_csv_files()
    # load_from_csv_to_database()
    print(os.urandom(12).hex())



