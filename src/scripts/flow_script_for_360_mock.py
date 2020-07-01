import datetime
import os
import pandas as pd

from config import engine
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
        'table_id': 'outcome_person_num#',  # "Outcome.Person.."
        'table_email': 'out_email',
        '_table_name': ['outcome_person_name'],
        '_preprocess': lambda df: match_data.group_concat(df, ['outcome_person_num', 'out_email', 'outcome_person_name'])
    },
    'volgistics': {
        '_label': 'volgistics',
        'table_id': 'number',
        'table_email': 'email',
        '_table_name': ['first_name_last_name']
    }
}  # TODO: consider other important fields, such as phone number



def start_flow():
    file_path_list = os.listdir(CURRENT_SOURCE_FILES_PATH)

    if file_path_list:
        rows_to_add_or_updated = load_paws_data.start(file_path_list, True)

        # rows_for_master_df = match_data.start(rows_to_add_or_updated)

        # create_master_df.start(rows_for_master_df)

        master_table_rows_array = []

        for i in range(len(rows_to_add_or_updated['new_rows']['salesforcecontacts'])):
            master_table_rows_array.append({
                'id': i,
                'salesforce_id': rows_to_add_or_updated['new_rows']['salesforcecontacts'][i]['contact_id'],
                'volgistics_id': rows_to_add_or_updated['new_rows']['volgistics'][i]['number'],
                'petpoint_id': rows_to_add_or_updated['new_rows']['petpoint'][i]['outcome_person_num']
            })

        df = pd.DataFrame(master_table_rows_array)

        df['created_date'] = datetime.datetime.now()
        df['deleted_date'] = None
        df.to_sql('master', engine, index=False)
