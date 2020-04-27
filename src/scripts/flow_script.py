import sys
import os

# get scripts folder to relative path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from scripts import load_paws_data, match_data, create_master_df

CURRENT_SOURCE_FILES_PATH = '/app/static/uploads/current'
UPLOADED_FILES_PATH = '/app/static/uploads/'
OUTPUT_PATH = "/app/static/output/"

MAPPING_FIELDS = {
    'salesforcecontacts': {
        '_label': 'salesforce',
        'table_id': 'contact_id',
        'table_email': 'email',
        '_table_name': ['first_name', 'last_name']
    },
    'petpoint': {
        '_label': 'petpoint',
        'table_id': 'outcome_person_#',
        'table_email': 'out_email',
        '_table_name': ['outcome_person_name']
    },
    'volgistics': {
        '_label': 'volgistics',
        'table_id': 'Number'.lower(),
        'table_email': 'Email'.lower(),
        '_table_name': ['first_name_last_name']
    }
}  # TODO: consider other important fields, such as phone number


def start_flow():
    if os.listdir(CURRENT_SOURCE_FILES_PATH):
        pandas_tables = dict()
        for uploaded_file in os.listdir(CURRENT_SOURCE_FILES_PATH):
            file_path = os.path.join(CURRENT_SOURCE_FILES_PATH, uploaded_file)
            file_name_striped = file_path.split('/')[-1].split('-')[0]
            print('running load_paws_data on: ' + uploaded_file)
            connection = load_paws_data.load_to_postgres(file_path, file_name_striped, True)
            # TODO: debug this
            pandas_tables[file_name_striped] = match_data.read_from_postgres(connection, file_name_striped)
            pandas_tables[file_name_striped] = match_data.cleanup_and_log_table(pandas_tables[file_name_striped],
                MAPPING_FIELDS[file_name_striped],
                                                                                'excluded_' + file_name_striped + '.csv')



        create_master_df.main(connection)


        matched_df = (
            pandas_tables['salesforcecontacts']
                .pipe(match_data.match_cleaned_table, pandas_tables['volgistics'], 'volgistics', 'unmatched_volgistics.csv')
        )

        matched_df.to_csv(os.path.join(match_data.LOG_PATH, 'matches.csv'), index=False)

        # connection.close()  # FIXME: how do you clean up a postgresql engine??  Automatic if you're not using the raw_connection?

