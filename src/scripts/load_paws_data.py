import pandas as pd
import re
import os

from config import engine
from flask import current_app
from config import CURRENT_SOURCE_FILES_PATH


def load_to_postgres(file_path_list, drop_first_col=False):
    result = {
        "new_rows": {},
        "updated_rows": {}
    }

    for uploaded_file in file_path_list:
        file_path = os.path.join(CURRENT_SOURCE_FILES_PATH, uploaded_file)
        table_name = file_path.split('/')[-1].split('-')[0]

        current_app.logger.info('running load_paws_data on: ' + uploaded_file)

        # connect to or create database
        # load csv into a dataframe
        df = pd.read_csv(file_path, encoding='cp1252')

        # drop the first column - so far all csvs have had a first column that's an index and doesn't have a name
        if drop_first_col:
            df = df.drop(df.columns[0], axis=1)

        # strip whitespace and periods from headers, convert to lowercase
        df.columns = df.columns.str.lower().str.strip()
        df.columns = df.columns.str.replace(' ', '_')
        df.columns = df.columns.map(lambda x: re.sub(r'\.+', '_', x))

        # temp table
        df.to_sql(table_name + '_temp', engine, index=False, if_exists='replace')
        __find_new_rows(result, table_name)

    return result
    
    # get conneciton from engine and use in with clause to automatically handle transaction cleanup
    '''with engine.connect() as connection:
        connection.execute(f'DROP TABLE IF EXISTS {table_name}')
        # load dataframe into database table
        current_app.logger.info('Creating table: ' + table_name)
        df.to_sql(table_name, engine, index=False,)
        current_app.logger.info('Finished creating generic table for: ' + table_name)'''


def __find_new_rows(found_rows, table_name):
    with engine.connect() as connection:
        if table_name == 'volgistics':
            rows = connection.execute('select * from {} t left join {} v on v.number = t.number where v.number is null'.format(table_name + "_temp", table_name))
            rows_data = []
            for row in rows:
                rows_data.append(row)
            found_rows['new_rows'] = {table_name: rows_data}





