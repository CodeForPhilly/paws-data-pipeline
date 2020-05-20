import shutil
import os
import time

from flask import send_file, render_template, request, redirect, flash, jsonify, Blueprint, current_app
from scripts import flow_script
from server.file_uploader import validate_and_arrange_upload
from config import UPLOAD_PATH, OUTPUT_PATH, CURRENT_SOURCE_FILES_PATH, ZIPPED_FILES, REPORT_PATH

ALLOWED_EXTENSIONS = {'csv'}

admin_api = Blueprint('admin_api', __name__)
common_api = Blueprint('common_api', __name__)


@admin_api.route('/', methods=['GET'])
def showIndexPage():
    current_file_list = listCurrentFiles().json

    # used in html
    output_files_exist = len(os.listdir(REPORT_PATH)) > 0

    return render_template('index.html', current_file_list=current_file_list, output_files_exist=output_files_exist)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# file upload tutorial
# https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
@admin_api.route('/file', methods=['POST'])
def uploadCSV():
    if 'file' not in request.files:
        flash('ERROR no file part', 'error')
        return redirect(request.url)

    for file in request.files.getlist('file'):
        if not allowed_file(file.filename):
            flash('ERROR not a csv: ' + file.filename, 'error')

        else:
            try:
                validate_and_arrange_upload(file, UPLOAD_PATH)
            except Exception as e:
                flash("ERROR can't parse upload: " + file.filename, 'error')
                current_app.logger.info(e)

            finally:
                file.close()

    return redirect('/')


@admin_api.route('/files/<destination>', methods=['GET'])
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


@admin_api.route('/listCurrentFiles', methods=['GET'])
def listCurrentFiles():
    result = None

    current_app.logger.info('Start returning file list')
    file_list_result = os.listdir(CURRENT_SOURCE_FILES_PATH)

    if len(file_list_result) > 0:
        result = file_list_result

    return jsonify(result)


@admin_api.route('/execute', methods=['GET'])
def execute():
    current_app.logger.info('Execute flow')
    flow_script.start_flow()
    flash('Successfully executed!', 'info')

    return showIndexPage()


@common_api.route('/time')
def get_current_time():
    return {'time': time.time()}