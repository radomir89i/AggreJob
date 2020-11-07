import io
import os

from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.discovery import build

from config import GoogleDrive, Config


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


def get_csv_files(target_folder=Config.EXPORT_FOLDER) -> None:

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





