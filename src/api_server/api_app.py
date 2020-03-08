import os
import flask
from flask import send_file, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import shutil
import sys

# get scripts folder to relative path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from scripts import sample_script
#need to use below import statement in windows environment
#import sample_script
import time

sys.path.insert(1, '../scripts')
dir_path = os.path.dirname(os.path.realpath(__file__))

SCRIPT_PATH = dir_path + '/../scripts'
DATA_FILES_PATH = '/app/static/uploads'
TEMPLATE_PATH = dir_path + '/../templates'
ALLOWED_EXTENSIONS = {'csv'}

SUCCESS_MSG = ' uploaded successfully! '

#TODO: this might not be enough as not all browsers properly detect file size
app = flask.Flask(__name__)
app.config['UPLOAD_FOLDER'] = DATA_FILES_PATH
app.secret_key = '1u9L#*&I3Ntc'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024 #500 Megs
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def showIndexPage():
    return render_template('index.html')

#file upload tutorial
#https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
@app.route('/', methods=['POST'])
def uploadCSV():
    if 'file' not in request.files:
        flash('ERROR no file part', 'error')
        return redirect(request.url)
    
    for file in request.files.getlist('file'):
        if not allowed_file(file.filename):
            flash('ERROR not a csv: ' + file.filename, 'error')
            continue
        try:
            column_header = file.stream.readline().decode('utf-8').split(',')[1].strip()
            valid_src = True
            if column_header == 'Account.Name':
                flash('Salesforce' + SUCCESS_MSG  + file.filename, 'info')
            elif column_header == 'Last.name..First.name':
                flash('Volgistics' + SUCCESS_MSG +  file.filename, 'info')
            elif column_header == 'Animal.ID':
                flash('Pet Point' + SUCCESS_MSG + file.filename, 'info')
            elif column_header == 'Recurring.donor':
                flash('Salesforce' + SUCCESS_MSG + file.filename, 'info')
            else:
                flash('ERROR Unrecognized data extract: ' + file.filename, 'error')
                valid_src = False
            if valid_src:
                filename = secure_filename(file.filename)
                prefix = filename.rpartition('.')[0]
                file_extension = filename.rpartition('.')[2]
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], prefix + '-' + str(round(time.time())) + '.' + file_extension))
        except:
            flash('ERROR can\'t parse upload: ' + file.filename, 'error')
            print(sys.exc_info()[0])
    
    return redirect('/')

@app.route('/listFiles', methods=['GET'])
def listFiles():
    print('Start returning file list')
    return str(os.listdir(DATA_FILES_PATH))


@app.route('/executeScript/<scriptName>', methods=['GET'])
def executeScript(scriptName):
    print('Start executing script: ' + scriptName)
    try:
        sample_script.run()
        return str(scriptName)

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
    app.run(debug = True)

