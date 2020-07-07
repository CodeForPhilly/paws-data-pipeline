import datetime
import pandas as pd
from config import engine
from flask import current_app


def __find_and_add_new_rows(connection, new_rows_dataframe):
    if new_rows_dataframe is not None:
        df_already_exists = engine.dialect.has_table(engine, 'master')

        # if the master_df table doesn't exist yet, create it from the new rows
        if not df_already_exists:
            current_app.logger.info('   - creating new master_df table')
            new_rows_dataframe['created_date'] = datetime.datetime.now()
            new_rows_dataframe['deleted_date'] = None
            new_rows_dataframe.to_sql('master', connection, index_label='master_id')
        # if the master_df table exists, append these rows to it
        else:
            current_app.logger.info('   - table exists. trying to add new rows')
            master_df = pd.read_sql('select * from master', connection)
            master_df.merge(new_rows_dataframe, how='outer')
            master_df.to_sql('master', connection, index_label='master_id', if_exists='replace') # TODO - master_id is getting duplicated. Fix this.


def __find_and_update_rows(connection, rows_to_update):
    if rows_to_update is None:
        return

    df_already_exists = engine.dialect.has_table(engine, 'master')
    if df_already_exists is False:
        current_app.logger.info('   - Error: tables were not added to master_df because it did not exist. Must create a new master_df using new_rows before updating those rows')
        return

    master_df = pd.read_sql('select * from master_df', connection)
    master_df.update(rows_to_update)
    master_df.to_sql('master', connection, index_label='master_id', if_exists='replace') # TODO - master_id is getting duplicated. Fix this.


def start(rows_for_master_df):
    # Create a simple table with the following values:
    # ------------> master_id (primary key), petpoint_id, volgistics_id, salesforce_id, created_date, deleted_date
    # petpoint[[outcome_person_id]]
    # volgistics[[number]]
    # salesforcecontacts[[account_id]]

    current_app.logger.info('Start creating Master table')

    # rows_for_master_df = {
    #     "new_rows": {},
    #     "updated_rows": {}
    # }

    new_rows_dataframe = None
    if "new_matches" in rows_for_master_df:
        new_rows_dataframe = pd.DataFrame(rows_for_master_df["new_matches"])

    updated_rows_dataframe = None
    if "updated_rows" in rows_for_master_df:
        updated_rows_dataframe = pd.DataFrame(rows_for_master_df["updated_rows"])

    with engine.connect() as connection:
        __find_and_add_new_rows(connection, new_rows_dataframe)

        # add updated rows (from 'updated_rows')
        __find_and_update_rows(connection, updated_rows_dataframe)

        current_app.logger.info('   - finish Create master table')
