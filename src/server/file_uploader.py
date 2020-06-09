import os
import time

from werkzeug.utils import secure_filename
from flask import flash, current_app
import pandas as pd

#TODO: Could we add sources dynamically?
TRACKED_COLUMNS = {
    'petpoint': ['Outcome Person #', 'Outcome Person Name', 'Out Street Address', 'Out Unit Number', 'Out City', 'Out Province', 'Out Postal Code', 'Out Email', 'Out Home Phone', 'Out Cell Phone'],
    'volgistics': ['Last name', 'First name', 'Middle name', 'Number', 'Complete address', 'Street 1', 'Street 2', 'Street 3', 'City', 'State', 'Zip', 'All phone numbers', 'Home', 'Work', 'Cell', 'Email'],
    'salesforcecontacts': ['Contact ID', 'First Name', 'Last Name', 'Mailing Street', 'Mailing City', 'Mailing State/Province', 'Mailing Zip/Postal Code', 'Mailing Country', 'Phone', 'Mobile', 'Email']
}

SUCCESS_MSG = 'Uploaded Successfully!'


def validate_and_arrange_upload(file, destination_path):
    current_app.logger.info("Start uploading file")
    src_type = determine_upload_type(file)

    if src_type:
        now = time.gmtime()
        now_date = time.strftime("%Y-%m-%d--%H-%M-%S", now)
        filename = secure_filename(file.filename)
        current_app.logger.info("  -File: " + filename + " Matches files type: " + src_type)

        file_extension = filename.rpartition('.')[2]
        file.stream.seek(0)
        file.save(os.path.join(destination_path, src_type + '-' + now_date + '.' + file_extension))

        current_app.logger.info('  -Checking if file of type: ' + src_type + ' already exists')
        clean_current_folder(destination_path + '/current', src_type)
        file.stream.seek(0)
        file.save(os.path.join(destination_path + '/current', src_type + '-' + now_date + '.' + file_extension))

        flash(src_type + " {0} ".format(SUCCESS_MSG), 'info')
        current_app.logger.info("  -Uploaded successfully as : " + src_type + '-' + now_date + '.' + file_extension)

    else:
        flash('ERROR Unrecognized data extract: ' + file.filename, 'error')


def determine_upload_type(file):
    df = pd.read_csv(file.stream)
    for key in TRACKED_COLUMNS:
        if set(TRACKED_COLUMNS[key]).issubset(df.columns):
            return key


def clean_current_folder(destination_path, src_type):
    if os.listdir(destination_path):
        for file_name in os.listdir(destination_path):
            file_path = os.path.join(destination_path, file_name)
            file_name_striped = file_path.split('-')[0].split('/')[-1]

            if file_name_striped == src_type:
                current_app.logger.info('File to remove: ' + file_path)
                os.remove(file_path)
                current_app.logger.info("  -Removed file: " + file_name + " from Current files folder")
