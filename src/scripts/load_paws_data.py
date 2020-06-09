import pandas as pd
import re
import os
import datetime

from config import engine
from flask import current_app
from config import CURRENT_SOURCE_FILES_PATH

TABLE_ID_MAPPING = {
    "volgistics": "number",
    "salesforcecontacts": "contact_id",
    "petpoint": "outcome_person_#"
}

TABLE_ID_MAPPING_V2 = {
    'volgistics': {'primary_key': 'number', 'tracked_columns': []},
    'salesforcecontacts': {'prmary_key': 'contact_id', 'tracked_columns': []},
    'petpoint': {'primary_key': 'outcome_person_', 'tracked_columns': []}
}


def start(file_path_list, should_drop_first_col=False):
    result = {
        "new_rows": {},
        "updated_rows": {}
    }

    for uploaded_file in file_path_list:
        file_path = os.path.join(CURRENT_SOURCE_FILES_PATH, uploaded_file)
        table_name = file_path.split('/')[-1].split('-')[0]

        current_app.logger.info('running load_paws_data on: ' + uploaded_file)

        df = pd.read_csv(file_path, encoding='cp1252')
        df = __clean_raw_data(df, should_drop_first_col)

        is_table_exist = __create_table(df, engine, table_name)

        if is_table_exist:
            current_app.logger.info('   - table exists. looking for new rows')
            df.to_sql(table_name + '_temp', engine, index=False, if_exists='replace')
            __find_and_add_new_rows(result, table_name)
        else:
            current_app.logger.info('   - creating new table')
            __add_rows_for_new_table(result, table_name)

        #todo: add logic for update - based on specific fields (list(df.columns.values))

        current_app.logger.info('   - finish load_paws_data on: ' + uploaded_file)

    return result


def __add_rows_for_new_table(found_rows, table_name):
    with engine.connect() as connection:
        # find new rows
        rows = connection.execute('select * from {}'.format(table_name)) #todo: fix for petpoint

        rows_data = []
        for row in rows:
            rows_data.append(row)

        found_rows['new_rows'][table_name] = rows_data


def __find_and_add_new_rows(found_rows, table_name):
    source_id = TABLE_ID_MAPPING[table_name]
    current_app.logger.info(table_name + ' ' + source_id)
    with engine.connect() as connection:
        # find new rows
        rows = connection.execute(
            'select * from {} t left join {} v on v."{}" = t."{}" where v."{}" is null'.format(
                table_name + "_temp", table_name, source_id, source_id, source_id))

        rows_data = []
        for row in rows:
            rows_data.append(row)

        found_rows['new_rows'] = {table_name: rows_data}

        # add new rows to data table
        connection.execute(
            'insert into {} \
             (select t.*, now() as created_date from {} t left join {} v on v."{}" = t."{}" where v."{}" is null)'.format(
                table_name, table_name + '_temp', table_name, source_id, source_id, source_id))

def __find_and_update_rows(found_rows, table_name):
    table_name_temp = table_name + '_temp'
    primary_key = ''
    tracked_columns = ''
    with engine.connect() as connection:
        updated_query = '''
            select * from {} where {} in (
                select {} from (
                    select {} 
                    from {} t 
                    where exists (select 1 from {} c where c.{} = t.{} and c.deleted_date is null)
                    except 
                    select {} 
                    from {} where deleted_date is null
            	) a
        )
        '''.format(table_name_temp, primary_key, primary_key, tracked_columns, table_name_temp, table_name, primary_key, primary_key, tracked_columns, table_name)
        #variables primary_key, tracked_columns[],
        rows = connection.execute(updated_query)
        row_data = []
        for row in rows:
            row_data.append(row)
        found_rows['updated_rows'] = {table_name: row_data}

def __create_table(df, engine, table_name):
    result = engine.dialect.has_table(engine, table_name)

    if not result:
        df['created_date'] = datetime.datetime.now()
        df['deleted_date'] = None
        df.to_sql(table_name, engine, index=False)

    return result


def __clean_raw_data(df, should_drop_first_col):
    # drop the first column - so far all csvs have had a first column that's an index and doesn't have a name
    if should_drop_first_col:
        df = df.drop(df.columns[0], axis=1)

    # strip whitespace and periods from headers, convert to lowercase
    df.columns = df.columns.str.lower().str.strip()
    df.columns = df.columns.str.replace(' ', '_')
    df.columns = df.columns.map(lambda x: re.sub(r'\.+', '_', x))

    return df
