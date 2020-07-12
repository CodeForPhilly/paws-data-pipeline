import datetime

import pandas as pd
from config import engine
from flask import current_app


def __find_and_add_new_rows(connection, new_rows_dataframe):
    current_app.logger.info('   - Adding new rows to master table')
    master_df = pd.read_sql('select * from master', connection)
    master_df = master_df.merge(new_rows_dataframe, how='outer')
    master_df['created_date'] = datetime.datetime.now()
    master_df.to_sql('master', connection, index_label='master_id', if_exists='replace') # TODO - master_id is getting duplicated. Fix this.


def __find_and_update_rows(connection, rows_to_update):
    current_app.logger.info('   - Updating rows to master table')
    master_df = pd.read_sql('select * from master', connection)
    master_df.update(rows_to_update)
    master_df.to_sql('master', connection, index_label='master_id', if_exists='replace') # TODO - master_id is getting duplicated. Fix this.


def start(rows_for_master_df):
    # Create a simple table with the following values:
    # ------------> master_id (primary key), petpoint_id, volgistics_id, salesforce_id, created_date, archived_date
    # petpoint[[outcome_person_id]]
    # volgistics[[number]]
    # salesforcecontacts[[account_id]]

    current_app.logger.info('Start creating Master table')

    with engine.connect() as connection:
        if "new_matches" in rows_for_master_df:
            new_rows_dataframe = pd.DataFrame(rows_for_master_df["new_matches"])
            __find_and_add_new_rows(connection, new_rows_dataframe)

        if "updated_rows" in rows_for_master_df:
            updated_rows_dataframe = pd.DataFrame(rows_for_master_df["updated_rows"])
            __find_and_update_rows(connection, updated_rows_dataframe)

        current_app.logger.info('   - Finish Creating master table')








