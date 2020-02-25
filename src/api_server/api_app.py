import os
import flask
from flask import send_file, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import shutil
import sys

# get scripts folder to relative path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
#from scripts import sample_script

sys.path.insert(1, '../scripts')
dir_path = os.path.dirname(os.path.realpath(__file__))

SCRIPT_PATH = dir_path + '/../scripts'
DATA_FILES_PATH = dir_path + '/../../sample_data'
TEMPLATE_PATH = dir_path + '/../templates'
UPLOAD_FOLDER = '/app/static/uploads'
ALLOWED_EXTENSIONS = {'csv'}

#TODO: this might not be enough as not all browsers properly detect file size
app = flask.Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = '1u9L#*&I3Ntc'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024

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
        flash('no file part')
        return redirect(request.url)
    
    file = request.files['file']
    if not allowed_file(file.filename):
        flash('not a csv')
        return redirect(request.url)
    #TODO: validate that it is from a correct source (Pet Point, Volgistics, Salesforce)
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    flash('csv successfully uploaded')
    
    return redirect('/')

@app.route('/listFiles', methods=['GET'])
def listFiles():
    print('Start returning file list')
    return str(os.listdir(DATA_FILES_PATH))


@app.route('/executeScript/<scriptName>', methods=['GET'])
def executeScript(scriptName):
    print('Start executing script: ' + scriptName)
    try:
        #sample_script.run()
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
        shutil.make_archive('data_out', 'zip', DATA_FILES_PATH)
        return send_file('data_out.zip', attachment_filename='data_out.zip')
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    app.run(debug = True)

