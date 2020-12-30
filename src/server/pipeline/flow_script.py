import os
import pandas as pd
from flask import current_app
from pipeline import calssify_new_data,clean_and_load_data, archive_rows
from config import CURRENT_SOURCE_FILES_PATH
from config import engine
from models import Base


def start_flow():
    file_path_list = os.listdir(CURRENT_SOURCE_FILES_PATH)

    if file_path_list:
        with engine.connect() as connection:
            Base.metadata.create_all(connection)

            pdp_contacts_df = pd.read_sql_table('pdp_contacts', connection)
            current_app.logger.info('Loaded {} records from pdp_contacts table'.format(pdp_contacts_df.shape[0]))

            # Clean the input data and normalize
            # input - existing files in path
            # output - normalized object of all entries
            normalized_data = clean_and_load_data.start(pdp_contacts_df, file_path_list)

            # Standardize column datatypes
            # If additional inconsistencies are encountered, may need to enforce the schema of
            # the contacts loader by initializing it from pdp_contacts.
            normalized_data.to_sql('_temp_pdp_contacts_loader', connection, index=False, if_exists='replace')
            normalized_data = pd.read_sql_table('_temp_pdp_contacts_loader', connection)

            # Classifies rows to old rows that haven't changed, updated rows and new rows - compared to the existing state of the DB
            rows_classified = calssify_new_data.start(pdp_contacts_df, normalized_data)

            # Archives rows the were updated in the current state of the DB (changes their archived_date to now)
            archive_rows.archive(connection, rows_classified["updated"])

            # todo: match and load
            #   Compare each new and updated item to all records in the DB
            #   (including all other items that are new and updated this iteration) - for each item:
            #       if it matches - it will get the same matching id as the match
            #       if it doesn't - generate matching id (some prefix with increment?)
            #       load it with created_at = now and archived_at = null

            ## test:
            current_app.logger.info('Writing pdp_contacts to PostgreSQL')
            current_app.logger.info(' - Columns: {}'.format(rows_classified["new"].columns))
            rows_classified["new"].to_sql('pdp_contacts', connection, index=False, if_exists='append')
            current_app.logger.info(' - Finished writing table')

