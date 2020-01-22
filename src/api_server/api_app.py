import os
import flask
from flask import send_file
import shutil

from ..scripts import sample_script

dir_path = os.path.dirname(os.path.realpath(__file__))

SCRIPT_PATH = dir_path + '/../scripts'
DATA_FILES_PATH = dir_path + '/../../sample_data'

app = flask.Flask(__name__)


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
        shutil.make_archive('data_out', 'zip', DATA_FILES_PATH)
        return send_file('data_out.zip', attachment_filename='data_out.zip')
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    app.run()

