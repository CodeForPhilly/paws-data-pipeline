import os
import time

from werkzeug.utils import secure_filename
from flask import flash

SRC_TYPES_BY_HEADER = {
    'Account.Name':          'salesforce_contacts',
    'Last.name..First.name': 'volgistics',
    'Animal.ID':             'petpoint',
    'Recurring.donor':       'salesforce_donations'
}

SUCCESS_MSG = 'Uploaded Successfully!'


def validate_and_arrange_upload(file, destination_path):
    src_type = determine_upload_type(file)

    if src_type:
        filename = secure_filename(file.filename)
        prefix = filename.rpartition('.')[0]
        file_extension = filename.rpartition('.')[2]
        file.stream.seek(0)
        file.save(os.path.join(destination_path, prefix + '-' + str(round(time.time())) + '.' + file_extension))

        flash(src_type + " {0} ".format(SUCCESS_MSG), 'info')

    else:
        flash('ERROR Unrecognized data extract: ' + file.filename, 'error')


def determine_upload_type(file):
    column_header = file.stream.readline().decode('utf-8').split(',')[1].strip()
    src_type = SRC_TYPES_BY_HEADER[column_header]

    return src_type
