import sys
import os

# get scripts folder to relative path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from scripts import load_paws_data

CURRENT_SOURCE_FILES_PATH = '/app/static/uploads/current'


def start_flow():
    if os.listdir(CURRENT_SOURCE_FILES_PATH):
        for uploaded_file in os.listdir(CURRENT_SOURCE_FILES_PATH):
            file_path = os.path.join(CURRENT_SOURCE_FILES_PATH, uploaded_file)
            file_name_striped = file_path.split('-')[0].split('/')[-1]
            print('running load_paws_data on: ' + uploaded_file)
            load_paws_data.load_to_sqlite(file_path, file_name_striped, True)
