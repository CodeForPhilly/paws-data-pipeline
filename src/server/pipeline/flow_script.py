import os
import pandas as pd
from flask import current_app
from pipeline import calssify_new_data, clean_and_load_data, archive_rows, match_data
from config import CURRENT_SOURCE_FILES_PATH
from config import engine
from models import Base


def start_flow():
    file_path_list = os.listdir(CURRENT_SOURCE_FILES_PATH)

    if file_path_list:
        with engine.connect() as connection:
            Base.metadata.create_all(connection)

            # Get previous version of pdp_contacts table, which is used later to classify new records
            pdp_contacts_df = pd.read_sql_table('pdp_contacts', connection)
            pdp_contacts_df = pdp_contacts_df[pdp_contacts_df["archived_date"].isnull()]
            pdp_contacts_df = pdp_contacts_df.drop(columns=['archived_date', 'created_date', '_id', 'matching_id'])

            current_app.logger.info('Loaded {} records from pdp_contacts table'.format(pdp_contacts_df.shape[0]))

            # Clean the input data and normalize/rename columns
            # Populate new records in secondary tables (donations, volunteer shifts)
            # input - existing files in path
            # output - normalized object of all entries, as well as the input json rows for primary sources
            normalized_data, source_json = clean_and_load_data.start(connection, pdp_contacts_df, file_path_list)

            # Standardize column data types via postgres (e.g. reading a csv column as int vs. str)
            # (If additional inconsistencies are encountered, may need to enforce the schema of
            # the contacts loader by initializing it from pdp_contacts.)
            normalized_data.to_sql('_temp_pdp_contacts_loader', connection, index=False, if_exists='replace')
            normalized_data = pd.read_sql_table('_temp_pdp_contacts_loader', connection)

            # Classifies rows to old rows that haven't changed, updated rows and new rows - compared to the existing state of the DB
            rows_classified = calssify_new_data.start(pdp_contacts_df, normalized_data)

            # Archives rows the were updated in the current state of the DB (changes their archived_date to now)
            archive_rows.archive(connection, rows_classified["updated"])

            # Match new+updated records against previous version of pdp_contacts database, and
            # write these rows to the database.
            match_data.start(connection, rows_classified)

            # TODO: also writing the json field from clean_and_load_data to the pdp_contacts table.
            # Will need to filter by source_type, source_id, and check that the rows are active by timestamp.
            # Maybe also an assert that all the records are properly identified (no missing IDs).
            # Might also need to remove the json field temporarily when doing the Venn diagram classification.
            print(source_json)  # writing source_json to update pdp_records table TODO

