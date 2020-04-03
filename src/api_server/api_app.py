import os
from flask import Flask, send_file, render_template, request, redirect, flash
import shutil
import sys

# get scripts folder to relative path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from scripts import flow_script
from api_server.file_uploader import validate_and_arrange_upload

sys.path.insert(1, '../scripts')
DATA_FILES_PATH = '/app/static/uploads'
ALLOWED_EXTENSIONS = {'csv'}

# TODO: this might not be enough as not all browsers properly detect file size
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = DATA_FILES_PATH
app.secret_key = '1u9L#*&I3Ntc'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500 Megs
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def showIndexPage():
    return render_template('index.html')


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
                print(e)

            finally:
                file.close()

    return redirect('/')


@app.route('/listFiles', methods=['GET'])
def listFiles():
    print('Start returning file list')
    return str(os.listdir(DATA_FILES_PATH))


@app.route('/execute/<fileName>', methods=['GET'])
def execute(fileName):
    print('Execute flow')
    try:
        flow_script.start_flow(fileName)
        flash('Successfully executed!', 'info')
        return ('Successfully executed flow script with file: ' + fileName)

    except Exception as e:
        return str(e)


@app.route('/file/<fileName>', methods=['GET'])
def file(fileName):
    print('Start returning file: ' + fileName)
    try:
        return send_file(DATA_FILES_PATH + '/' + fileName, attachment_filename=fileName)
    except Exception as e:
        return str(e)


@app.route('/allFiles', methods=['GET'])
def allFiles():
    print('Start returning zip of all data')
    try:
        print(shutil.make_archive('data_out', 'zip', DATA_FILES_PATH))
        return send_file('/paws-data-pipeline/data_out.zip', as_attachment=True, attachment_filename='data_out.zip')
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    app.run(debug=True)
