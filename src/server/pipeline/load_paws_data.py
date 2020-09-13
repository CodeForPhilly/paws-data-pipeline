import pandas as pd
import re
import os
import io
import datetime

from datasource_manager import DATASOURCE_MAPPING
from flask import current_app
from config import CURRENT_SOURCE_FILES_PATH
from datetime import datetime
from models import Base


def start(connection, file_path_list, should_drop_first_col=False):
    result = {
        "new_rows": {},
        "updated_rows": {}
    }
    for uploaded_file in file_path_list:
        file_path = os.path.join(CURRENT_SOURCE_FILES_PATH, uploaded_file)
        table_name = file_path.split('/')[-1].split('-')[0]
        current_app.logger.info('   - Running load_paws_data on: ' + uploaded_file)

        df = pd.read_csv((io.BytesIO(open(file_path, "rb").read())), encoding='iso-8859-1')
        current_app.logger.info('   - Populated DF')

        df = __clean_raw_data(df, should_drop_first_col)
        _dict = {c.name: c.type for c in Base.metadata.tables[table_name].c}
        current_app.logger.info('   - Built schema dict')

        df.to_sql(table_name + '_stage', connection, index=False, if_exists='replace', dtype=_dict)
        ##current_app.logger.info('   - Looking for updated rows ')
        #__find_updated_rows(connection, result, table_name)
        current_app.logger.info('   - Looking for new rows ')

        __find_new_rows(connection, result, table_name)
        current_app.logger.info('   - Finish load_paws_data on: ' + uploaded_file)

    return result


def __find_new_rows(connection, result, table_name):
    source_id = DATASOURCE_MAPPING[table_name]['id']
    current_app.logger.info(table_name + ' ' + source_id)
    # find new rows
    rows = connection.execute(
        'select t.* from {} t left join {} c on c."{}" = t."{}" where c."{}" is null'.format(
            table_name + "_stage", table_name, source_id, source_id, source_id))
            
    rows_data = []
    now = datetime.now()
    tracked_columns = DATASOURCE_MAPPING[table_name]['tracked_columns']

    for row in rows:
        row_dict = {}
        json_dict = {}

        for key_value in row.items():
            if key_value[0] in tracked_columns:
                if key_value[0] == DATASOURCE_MAPPING['volgistics']['id']:
                    row_dict[key_value[0]] = str(key_value[1])
                else:
                    row_dict[key_value[0]] = key_value[1]
            json_dict[key_value[0]] = key_value[1]

        row_dict['json'] = json_dict
        row_dict['created_date'] = now
        rows_data.append(row_dict)

    result['new_rows'][table_name] = rows_data
    ins = Base.metadata.tables[table_name].insert()
    connection.execute(ins, rows_data)


def __find_updated_rows(connection, found_rows, table_name):
    table_name_temp = table_name + '_stage'
    primary_key = DATASOURCE_MAPPING[table_name]['id']
    tracked_columns = DATASOURCE_MAPPING[table_name]['tracked_columns']
    tracked_column_str = ''
    for column in tracked_columns:
        tracked_column_str += '"' + column + '", '
    tracked_column_str = tracked_column_str[:-2]

    # find updated rows
    updated_query = '''
        select * from {} where "{}" in (
            select "{}" from (
                select {} 
                from {} t 
                where exists (select 1 from {} c where c."{}" = t."{}" and c.archived_date is null)
                except 
                select {} 
                from {} where archived_date is null
            ) a
    )
    '''.format(table_name_temp, primary_key, primary_key, tracked_column_str, table_name_temp, table_name,
               primary_key, primary_key, tracked_column_str, table_name)
    rows = connection.execute(updated_query)
    row_data = __create_row_dicts(rows, tracked_columns)

    if row_data:
        updates = {table_name: row_data}
        found_rows['updated_rows'] = updates

    # mark old version of updated rows as archived
    mark_deleted = '''
    update {} set archived_date = now() where "{}" in (
        select "{}" from (
            select {}
            from {} t 
            where exists (select 1 from {} c where c."{}" = t."{}" and c.archived_date is null)
            except 
            select {}
            from {} where archived_date is null
        ) a
    ) and archived_date is null
    '''.format(table_name, primary_key, primary_key, tracked_column_str, table_name_temp, table_name, primary_key,
               primary_key, tracked_column_str, table_name)
    connection.execute(mark_deleted)

    # insert new updated rows ....eeek that's confusing
    ins = Base.metadata.tables[table_name].insert()
    connection.execute(ins, row_data)


def __create_row_dicts(rows, tracked_columns):
    rows_data = []
    now = datetime.now()
    for row in rows:
        row_dict = {}
        json_dict = {}
        for key_value in row.items():
            if key_value[0] in tracked_columns:
                row_dict[key_value[0]] = key_value[1]
            json_dict[key_value[0]] = key_value[1]
        row_dict['json'] = json_dict
        row_dict['created_date'] = now
        rows_data.append(row_dict)
    return rows_data


def __clean_raw_data(df, should_drop_first_col):
    # drop the first column - so far all csvs have had a first column that's an index and doesn't have a name
    if should_drop_first_col:
        df = df.drop(df.columns[0], axis=1)

    # strip whitespace and periods from headers, convert to lowercase
    df.columns = df.columns.str.replace(r"\.*\(%\)\.*", "")
    df.columns = df.columns.str.lower().str.strip()
    df.columns = df.columns.str.replace(' ', '_')
    df.columns = df.columns.str.replace('#', 'num')
    df.columns = df.columns.str.replace('/', '_')
    df.columns = df.columns.map(lambda x: re.sub(r'\.+', '_', x))

    return df
