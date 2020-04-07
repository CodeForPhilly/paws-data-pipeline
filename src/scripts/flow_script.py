import sys
import os

# get scripts folder to relative path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from scripts import load_paws_data

UPLOADED_FILES_PATH = '/app/static/uploads/'

def start_flow(fileName):
    load_paws_data.load_to_sqlite(UPLOADED_FILES_PATH + fileName, 'salesforcecontacts', True)
