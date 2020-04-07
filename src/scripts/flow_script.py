import sys
import os

# get scripts folder to relative path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from scripts import load_paws_data, match_data

CURRENT_SOURCE_FILES_PATH = '/app/static/uploads/current'
UPLOADED_FILES_PATH = '/app/static/uploads/'

MAPPING_FIELDS = {
    'salesforcecontacts': {
        '_label':      'salesforce',
        'table_id':    'contact_id',
        'table_email': 'email',
        '_table_name': ['first_name', 'last_name']
    },
    'volgistics':         {
        '_label':      'volgistics',
        'table_id':    'outcome_person_#',
        'table_email': 'out_email',
        '_table_name': ['outcome_person_name']
    }
}


# TODO: consider other important fields, such as phone number


def start_flow():
    if os.listdir(CURRENT_SOURCE_FILES_PATH):
        pandas_tables = dict()
        for uploaded_file in os.listdir(CURRENT_SOURCE_FILES_PATH):
            file_path = os.path.join(CURRENT_SOURCE_FILES_PATH, uploaded_file)
            file_name_striped = file_path.split('-')[0].split('/')[-1]
            print('running load_paws_data on: ' + uploaded_file)
            load_paws_data.load_to_sqlite(file_path, file_name_striped, True)
            pandas_tables[file_name_striped] = match_data.read_from_sqlite(file_name_striped)
            pandas_tables[file_name_striped] = match_data.cleanup_and_log_table(pandas_tables[file_name_striped],
                                                                                MAPPING_FIELDS[file_name_striped],
                                                                                'excluded_' + file_name_striped + '.csv')
        matched_df = (
            pandas_tables['salesforcecontacts']
                .pipe(match_data.match_cleaned_table, pandas_tables['volgistics'], 'volgistics',
                      'unmatched_volgistics.csv')
        )
        matched_df.to_csv(os.path.join(match_data.LOG_PATH, 'matches.csv'), index=False)
