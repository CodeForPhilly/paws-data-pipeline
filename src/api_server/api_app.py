import os
from flask import Flask, send_file, render_template, request, redirect, flash, jsonify
import shutil
import sys
import traceback

# get scripts folder to relative path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from scripts import flow_script
from api_server.file_uploader import validate_and_arrange_upload

sys.path.insert(1, '../scripts')
SOURCE_FILES_PATH = '/app/static/uploads'
OUTPUT_FILES_PATH = '/app/static/output'
ALLOWED_EXTENSIONS = {'csv'}

# TODO: this might not be enough as not all browsers properly detect file size
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = SOURCE_FILES_PATH
app.secret_key = '1u9L#*&I3Ntc'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500 Megs
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route('/', methods=['GET'])
def showIndexPage():
    current_file_list = listCurrentFiles().json
    output_files_exist = len(os.listdir(OUTPUT_FILES_PATH)) > 0

    return render_template('index.html', current_file_list=current_file_list, output_files_exist=output_files_exist)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# file upload tutorial
# https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
@app.route('/file', methods=['POST'])
def uploadCSV():
    if 'file' not in request.files:
        flash('ERROR no file part', 'error')
        return redirect(request.url)

    for file in request.files.getlist('file'):
        if not allowed_file(file.filename):
            flash('ERROR not a csv: ' + file.filename, 'error')

        else:
            try:
                validate_and_arrange_upload(file, app.config['UPLOAD_FOLDER'])
            except Exception as e:
                flash("ERROR can't parse upload: " + file.filename, 'error')
                app.logger.info(e)

            finally:
                file.close()

    return redirect('/')


@app.route('/files/<destination>', methods=['GET'])
def files(destination):
    app.logger.info('Start returning zip of all data')
    if request.args.get('download_current_btn'):
        source = SOURCE_FILES_PATH + '/' + destination
    if request.args.get('download_archived_btn'):
        source = SOURCE_FILES_PATH
    if request.args.get('download_output_btn'):
        source = OUTPUT_FILES_PATH

    zip_name = destination + '_data_out'

    try:
        app.logger.info(shutil.make_archive(zip_name, 'zip', source))
        return send_file('/paws-data-pipeline/' + zip_name + '.zip', as_attachment=True,
                         attachment_filename=zip_name + '.zip')
    except Exception as e:
        return str(e)


@app.route('/listCurrentFiles', methods=['GET'])
def listCurrentFiles():
    result = None

    app.logger.info('Start returning file list')
    file_list_result = os.listdir(SOURCE_FILES_PATH + '/current')

    if len(file_list_result) > 0:
        result = file_list_result

    return jsonify(result)


@app.route('/execute', methods=['GET'])
def execute():
    app.logger.info('Execute flow')
    flow_script.start_flow()
    flash('Successfully executed!', 'info')
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
