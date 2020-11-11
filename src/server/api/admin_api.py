from api.api import admin_api
import shutil
import os
from datetime import datetime
import json
from sqlalchemy.sql import text

from config import engine
from flask import send_file, request, redirect, jsonify, current_app
from api.file_uploader import validate_and_arrange_upload
from config import UPLOAD_PATH, OUTPUT_PATH, CURRENT_SOURCE_FILES_PATH, ZIPPED_FILES, LOGS_PATH

ALLOWED_EXTENSIONS = {'csv', 'xlsx'}

def __allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# file upload tutorial
@admin_api.route('/api/file', methods=['POST'])
def uploadCSV():
    if 'file' not in request.files:
        return redirect(request.url)

    for file in request.files.getlist('file'):
        if __allowed_file(file.filename):
            try:
                validate_and_arrange_upload(file, UPLOAD_PATH)
            except Exception as e:
                current_app.logger.exception(e)
            finally:
                file.close()

    return redirect('/')


@admin_api.route('/api/files/<destination>', methods=['GET'])
def files(destination):
    current_app.logger.info('Start returning zip of all data')
    if request.args.get('download_current_btn'):
        source = UPLOAD_PATH + destination
    if request.args.get('download_archived_btn'):
        source = UPLOAD_PATH
    if request.args.get('download_output_btn'):
        source = OUTPUT_PATH

    zip_name = destination + '_data_out'

    try:
        current_app.logger.info(shutil.make_archive(ZIPPED_FILES + zip_name, 'zip', source))
        return send_file(ZIPPED_FILES + zip_name + '.zip', as_attachment=True,
                         attachment_filename=zip_name + '.zip')
    except Exception as e:
        return str(e)


@admin_api.route('/api/listCurrentFiles', methods=['GET'])
def listCurrentFiles():
    result = None

    current_app.logger.info('Start returning file list')
    file_list_result = os.listdir(CURRENT_SOURCE_FILES_PATH)

    if len(file_list_result) > 0:
        result = file_list_result

    return jsonify(result)


@admin_api.route('/api/execute', methods=['GET'])
def execute():
    current_app.logger.info('Execute flow')
    #flow_script.start_flow()

    current_time = datetime.now().ctime()
    statistics = getStatistics()

    last_execution_details = {
        "executionTime": current_time,
        "stats": statistics
    }

    last_execution_file = open(LOGS_PATH + 'last_execution.json', 'w')
    last_execution_file.write(json.dumps(last_execution_details))
    last_execution_file.close()

    return jsonify(success=True)


'''
@admin_api.route('/api/status', methods=['GET'])
def checkStatus():
    with engine.connect() as connection:
        query = text("SELECT now()")
        query_result = connection.execute(query)

        # Need to iterate over the results proxy
        results = {}
        for row in query_result:
            results = dict(row)
        return jsonify(results)
'''



@admin_api.route('/api/statistics', methods=['GET'])
def listStatistics():
    last_execution_file = open(LOGS_PATH + 'last_execution.json', 'r')
    last_execution_details = json.loads(last_execution_file.read())
    last_execution_file.close()

    return jsonify(last_execution_details)


def getStatistics():
    with engine.connect() as connection:
        query = text("SELECT \
            SUM(CASE WHEN salesforcecontacts_id is not null and volgistics_id is null and petpoint_id is null THEN 1 ELSE 0 END) AS \"Only SalesForce Contacts\", \
            SUM(CASE WHEN volgistics_id is not null and petpoint_id is null and salesforcecontacts_id is null THEN 1 ELSE 0 END) AS \"Only Volgistics Contacts\", \
            SUM(CASE WHEN petpoint_id is not null and volgistics_id is null and salesforcecontacts_id is null THEN 1 ELSE 0 END) AS \"Only Petpoint Contacts\", \
            SUM(CASE WHEN salesforcecontacts_id is not null and petpoint_id is not null and volgistics_id is null THEN 1 ELSE 0 END) AS \"Salesforcec & Petpoint\", \
            SUM(CASE WHEN salesforcecontacts_id is not null and volgistics_id is not null and petpoint_id is null THEN 1 ELSE 0 END) AS \"Salesforce & Volgistics\", \
            SUM(CASE WHEN volgistics_id is not null and petpoint_id is not null and salesforcecontacts_id is null THEN 1 ELSE 0 END) AS \"Petpoint & Volgistics\", \
            SUM(CASE WHEN salesforcecontacts_id is not null and volgistics_id is not null and petpoint_id is not null THEN 1 ELSE 0 END) AS \"Salesforcec & Petpoint & Volgistics\" \
            FROM master")
        query_result = connection.execute(query)

        # Need to iterate over the results proxy
        results = {}
        for row in query_result:
            results = dict(row)

        return results
