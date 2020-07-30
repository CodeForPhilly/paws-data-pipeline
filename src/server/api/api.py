import shutil
import os

from flask import send_file, request, redirect, jsonify, Blueprint, current_app
from scripts import flow_script
from api.file_uploader import validate_and_arrange_upload
from config import UPLOAD_PATH, OUTPUT_PATH, CURRENT_SOURCE_FILES_PATH, ZIPPED_FILES

ALLOWED_EXTENSIONS = {'csv', 'xlsx'}

admin_api = Blueprint('admin_api', __name__)
common_api = Blueprint('common_api', __name__)

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
    flow_script.start_flow()

    return jsonify(success=True)

