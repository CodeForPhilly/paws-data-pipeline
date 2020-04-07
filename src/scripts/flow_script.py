import sys
import os

# get scripts folder to relative path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from scripts import load_paws_data, match_data

CURRENT_SOURCE_FILES_PATH = '/app/static/uploads/current'
UPLOADED_FILES_PATH = '/app/static/uploads/'

SALESFORCE_FIELDS = {'_label': 'salesforce', 'table_id': 'contact_id', 'table_email': 'email', '_table_name': ['first_name', 'last_name']}
VOLGISTICS_FIELDS = {'_label': 'volgistics', 'table_id': 'outcome_person_#', 'table_email': 'out_email', '_table_name': ['outcome_person_name']}
# TODO: consider other important fields, such as phone number


def start_flow():
    if os.listdir(CURRENT_SOURCE_FILES_PATH):
        for uploaded_file in os.listdir(CURRENT_SOURCE_FILES_PATH):
            file_path = os.path.join(CURRENT_SOURCE_FILES_PATH, uploaded_file)
            file_name_striped = file_path.split('-')[0].split('/')[-1]
            print('running load_paws_data on: ' + uploaded_file)
            load_paws_data.load_to_sqlite(file_path, file_name_striped, True)


    '''
    # FIXME: need some logic to determine the table type, such as salesforce/volgistics/petpoint
    load_paws_data.load_to_sqlite(UPLOADED_FILES_PATH + fileName, 'salesforcecontacts', True)
    salesforce_contacts = match_data.read_from_sqlite('salesforcecontacts')
    salesforce_contacts = match_data.cleanup_and_log_table(salesforce_contacts, SALESFORCE_FIELDS, 'excluded_salesforce.csv')

    load_paws_data.load_to_sqlite('volgistics_path.csv', 'volgistics', True)
    volgistics_df = match_data.read_from_sqlite('volgistics')
    volgistics_df = match_data.cleanup_and_log_table(volgistics_df, VOLGISTICS_FIELDS, 'excluded_volgistics.csv')

    matched_df = (
        salesforce_contacts
        .pipe(match_data.match_cleaned_table, volgistics_df, 'volgistics.csv', 'unmatched_volgistics.csv')
        # TODO: also pipe other cleaned tables to match, such as petpoint, here
    )
    matched_df.to_csv(os.path.join(match_data.LOG_PATH, 'matches.csv'), index=False)
    '''
