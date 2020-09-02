import os
import time
import pandas as pd
import threading

from werkzeug.utils import secure_filename
from flask import flash, current_app
from datasource_manager import CSV_HEADERS
from datasource_manager import DATASOURCE_MAPPING
from openpyxl import load_workbook
from tempfile import NamedTemporaryFile

SUCCESS_MSG = 'Uploaded Successfully!'
lock = threading.Lock()

def validate_and_arrange_upload(file, destination_path):
    current_app.logger.info("Start uploading file: " + file.filename)
    filename = secure_filename(file.filename)
    file_extension = filename.rpartition('.')[2]
    determine_upload_type(file, file_extension, destination_path)

def determine_upload_type(file, file_extension, destination_path):
    if file_extension == 'csv':
        dfs = []
        df = pd.read_csv(file.stream, encoding='iso-8859-1')
        dfs.append(df)
        file.close()
    else:
        dfs = excel_to_dataframes(file)
    for src_type in CSV_HEADERS:
        for df in dfs:
            if set(CSV_HEADERS[src_type]).issubset(df.columns):
                with lock:
                    filename = secure_filename(file.filename)
                    now = time.gmtime()
                    now_date = time.strftime("%Y-%m-%d--%H-%M-%S", now)
                    current_app.logger.info("  -File: " + filename + " Matches files type: " + src_type)
                    df.to_csv(os.path.join(destination_path, src_type + '-' + now_date + '.csv'))
                    clean_current_folder(destination_path + '/current', src_type)
                    df.to_csv(os.path.join(destination_path + '/current', src_type + '-' + now_date + '.csv'))
                    current_app.logger.info("  -Uploaded successfully as : " + src_type + '-' + now_date + '.' + file_extension)
                    flash(src_type + " {0} ".format(SUCCESS_MSG), 'info')
    flash('ERROR Unrecognized data extract: ' + file.filename, 'error')

def excel_to_dataframes(xls):
    wb = load_workbook(xls)
    with NamedTemporaryFile() as tmp:
        wb.save(tmp.name)
        for sheetname in wb.sheetnames:
            for item in DATASOURCE_MAPPING:
                if item['sheetname'] == sheetname:
                    tmp.seek(0)
                    df = pd.read_excel(tmp.read(), sheetname)
                    return df

def clean_current_folder(destination_path, src_type):
    if os.listdir(destination_path):
        for file_name in os.listdir(destination_path):
            file_path = os.path.join(destination_path, file_name)
            file_name_striped = file_path.split('-')[0].split('/')[-1]

            if file_name_striped == src_type:
                current_app.logger.info('File to remove: ' + file_path)
                os.remove(file_path)
                current_app.logger.info("  -Removed file: " + file_name + " from Current files folder")
