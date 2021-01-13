import io
import os

from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from googleapiclient.discovery import build

from config import GoogleDrive, Config


service = build('drive', 'v3', credentials=GoogleDrive.GD_CREDENTIALS)

gdrive_file_list = service \
    .files() \
    .list(
        pageSize=1000,
        fields='nextPageToken, files(id, name, mimeType)') \
    .execute()['files']


def upload_file(file_path: str) -> None:

    """
    Uploads target file to GoogleDrive
    """

    file_metadata = {
        'name': os.path.basename(file_path),
        'parents': [GoogleDrive.FOLDER_ID],
        'mimeType': 'text/csv',
    }
    media = MediaFileUpload(file_path, resumable=True)
    service.files().create(body=file_metadata, media_body=media, fields='id').execute()


def upload_csv_files(target_folder=Config.EXPORT_FOLDER) -> None:

    """
    Uploads all *.csv files from target folder to GoogleDrive
    """

    files = [os.path.join(target_folder, f) for f in os.listdir(target_folder) if f.endswith('.csv')]
    for file in files:
        file_metadata = {
            'name': os.path.basename(file),
            'parents': [GoogleDrive.FOLDER_ID],
            'mimeType': 'text/csv',
        }
        media = MediaFileUpload(file, resumable=True)
        service.files().create(body=file_metadata, media_body=media, fields='id').execute()


def delete_csv_files() -> None:

    """
    Deletes all *.csv files in Google Drive folder.
    """

    for file in gdrive_file_list:
        if file['mimeType'] == 'text/csv':
            service.files().delete(fileId=file['id']).execute()


def get_csv_files(target_folder=Config.EXPORT_FOLDER) -> None:

    """
    Gets all *.csv files from Google Drive folder and puts them in target folder.
    :param target_folder: path to folder where downloaded files should be placed
    """

    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    for file in gdrive_file_list:
        if file['mimeType'] == 'text/csv':
            request = service.files().get_media(fileId=file['id'])
            fh = io.FileIO(os.path.join(target_folder, file['name']), 'wb')
            downloader = MediaIoBaseDownload(fh, request)

            done = False
            while not done:
                status, done = downloader.next_chunk()
                print("Download %d%%." % int(status.progress() * 100))




