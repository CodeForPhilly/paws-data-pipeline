import sys
import os

# get scripts folder to relative path
#sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
# FIXME: Python module paths seem particularly hacky, so come back and fix this part later
#sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
#sys.path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
#print(sys.path)
#print(__file__)
#import scripts
#print(dir(scripts))

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from scripts import load_paws_data, match_data

UPLOADED_FILES_PATH = '/app/static/uploads/'

SALESFORCE_FIELDS = {'_label': 'salesforce', 'table_id': 'contact_id', 'table_email': 'email', '_table_name': ['first_name', 'last_name']}
VOLGISTICS_FIELDS = {'_label': 'volgistics', 'table_id': 'outcome_person_#', 'table_email': 'out_email', '_table_name': ['outcome_person_name']}
# TODO: consider other important fields, such as phone number


def start_flow(fileName):
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


#start_flow('Salesforce - Accounts and Contacts.csv')
