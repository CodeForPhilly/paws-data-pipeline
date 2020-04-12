import os
import time

from werkzeug.utils import secure_filename
from flask import flash

SRC_TYPES_BY_HEADER = {
    'Account.Name':          'salesforcecontacts',
    'Last.name..First.name': 'volgistics',
    'Animal.ID':             'petpoint',
    'Recurring.donor':       'salesforcedonations'
}

SUCCESS_MSG = 'Uploaded Successfully!'


def validate_and_arrange_upload(file, destination_path):
    src_type = determine_upload_type(file)
    print("Start uploading file")

    if src_type:
        now = time.gmtime()
        now_date = time.strftime("%Y-%m-%d--%H-%M-%S", now)
        filename = secure_filename(file.filename)
        print("  -" + filename)

        file_extension = filename.rpartition('.')[2]
        file.stream.seek(0)
        file.save(os.path.join(destination_path, src_type + '-' + now_date + '.' + file_extension))

        print('Checking if file of type: ' + src_type + ' already exists')
        clean_current_folder(destination_path + '/current', src_type)
        file.stream.seek(0)
        file.save(os.path.join(destination_path + '/current', src_type + '-' + now_date + '.' + file_extension))

        flash(src_type + " {0} ".format(SUCCESS_MSG), 'info')
        print("  -Uploaded successfully!")

    else:
        flash('ERROR Unrecognized data extract: ' + file.filename, 'error')


def determine_upload_type(file):
    column_header = file.stream.readline().decode('utf-8').split(',')[1].strip()
    str('column_header is: ' + column_header)
    src_type = SRC_TYPES_BY_HEADER[column_header]

    return src_type


def clean_current_folder(destination_path, src_type):
    if os.listdir(destination_path):
        for file_name in os.listdir(destination_path):
            file_path = os.path.join(destination_path, file_name)
            file_name_striped = file_path.split('-')[0].split('/')[-1]

            if file_name_striped == src_type:
                print('file to remove: ' + file_path)
                os.remove(file_path)
                print("  -Removed file: " + file_name + " from Current files folder")
