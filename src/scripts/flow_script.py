import os

from scripts import load_paws_data, match_data, create_master_df
from config import CURRENT_SOURCE_FILES_PATH

MAPPING_FIELDS = {
    'salesforcecontacts': {
        '_label': 'salesforce',
        'table_id': 'contact_id',
        'table_email': 'email',
        '_table_name': ['first_name', 'last_name']
    },
    'petpoint': {
        '_label': 'petpoint',
        'table_id': 'outcome_person_',  # "Outcome.Person.."
        'table_email': 'out_email',
        '_table_name': ['outcome_person_name'],
        '_preprocess': lambda df: match_data.group_concat(df, ['outcome_person_', 'out_email', 'outcome_person_name'])
    },
    'volgistics': {
        '_label': 'volgistics',
        'table_id': 'Number'.lower(),
        'table_email': 'Email'.lower(),
        '_table_name': ['first_name_last_name']
    }
}  # TODO: consider other important fields, such as phone number


def start_flow():
    file_path_list = os.listdir(CURRENT_SOURCE_FILES_PATH)

    if file_path_list:
        rows_to_add_or_updated = load_paws_data.start(file_path_list, True)

        # rows_for_master_df = match_data.start(rows_to_add_or_updated)

        rows_for_master_df = {'new_matches': [
            {'salesforce_id': '00339000029jzJn', 'volgistics_id': '8362124',
             'petpoint_id': 'P100'},
            {'salesforce_id': '00339000029k20k', 'volgistics_id': '6011436',
             'petpoint_id': 'P200'},
            {'salesforce_id': '0033900002A03Vy', 'volgistics_id': '8249492',
             'petpoint_id': 'P300'}
            #{'salesforce_id': '1', 'volgistics_id': '2',
            #'petpoint_id': '3'}
        ]}

        create_master_df.start(rows_for_master_df)
