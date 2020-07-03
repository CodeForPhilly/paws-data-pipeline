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
        'table_id': 'outcome_person_num',  # "Outcome.Person.."
        'table_email': 'out_email',
        '_table_name': ['outcome_person_name'],
        '_preprocess': lambda df: match_data.group_concat(df, ['outcome_person_num', 'out_email', 'outcome_person_name'])
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

        rows_for_master_df = match_data.start(rows_to_add_or_updated)

        #create_master_df.start(rows_for_master_df)
