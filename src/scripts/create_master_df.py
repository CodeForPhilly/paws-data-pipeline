import datetime

import pandas as pd

from flask import current_app


def __find_and_add_new_rows(connection, new_rows_dataframe):
    current_app.logger.info('   - Adding new rows to master table')
    master_df = pd.read_sql('select * from master', connection)
    master_df = master_df.merge(new_rows_dataframe, how='outer')
    master_df['created_date'] = datetime.datetime.now()
    master_df.to_sql('master', connection, index=False, if_exists='replace')


def __find_and_update_rows(connection, rows_to_update):
    current_app.logger.info('   - Updating rows to master table')
    master_df = pd.read_sql('select * from master', connection)
    master_df.update(rows_to_update)
    master_df.to_sql('master', connection, index=False, if_exists='replace')


def __create_new_user(connection, master_id, name, email, source):
    # TODO: Take a list of users
    current_app.logger.info('   - Creating new User')
    user_df = pd.read_sql(
        'select * from user_info',
        connection
    )
    user_id = None
    try:
        user_id = user_df[user_df.master_id == master_id][user_df.source == source]['_id'][0]
    except KeyError:
        pass

    if user_id is not None:
        new_user = pd.DataFrame({
            '_id': [user_id],
            'master_id': [master_id],
            'name': [name],
            'email': [email],
            'source': [source]
        })
    else:
        new_user = pd.DataFrame({
            'master_id': [master_id],
            'name': [name],
            'email': [email],
            'source': [source]
        })
    user_df.update(new_user)
    user_df.to_sql('user', connection, index=False, if_exists='replace')


def start(connection, rows_for_master_df):
    # Create a simple table with the following values:
    # ------------> master_id (primary key), petpoint_id, volgistics_id, salesforce_id, created_date, archived_date
    # petpoint[[outcome_person_id]]
    # volgistics[[number]]
    # salesforcecontacts[[account_id]]

    current_app.logger.info('Start creating Master table')

    if "new_matches" in rows_for_master_df:
        new_rows_dataframe = pd.DataFrame(rows_for_master_df["new_matches"])
        __find_and_add_new_rows(connection, new_rows_dataframe)

    if "updated_rows" in rows_for_master_df:
        updated_rows_dataframe = pd.DataFrame(rows_for_master_df["updated_rows"])
        __find_and_update_rows(connection, updated_rows_dataframe)

    current_app.logger.info('   - Finish Creating master table')
