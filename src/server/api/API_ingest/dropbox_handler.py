import dropbox
from secrets import DROPBOX_APP


class TransferData:
    def __init__(self, access_token):
        self.access_token = access_token

    def upload_file(self, file_from, file_to):
        dbx = dropbox.Dropbox(self.access_token)

        with open(file_from, 'rb') as f:
            dbx.files_upload(f.read(), file_to)


def upload_file_to_dropbox(file_path, upload_path):
    access_token = DROPBOX_APP
    transfer_data = TransferData(access_token)

    file_from = file_path
    file_to = upload_path  # The full path to upload the file to, including the file name

    transfer_data.upload_file(file_from, file_to)