import pandas as pd
import re
import os
import io
import datetime

from datasource_manager import DATASOURCE_MAPPING, SOURCE_NORMALIZATION_MAPPING
from flask import current_app
from config import CURRENT_SOURCE_FILES_PATH
from datetime import datetime
from models import Base


def start(connection, file_path_list):
    result = {}

    for uploaded_file in file_path_list:
        file_path = os.path.join(CURRENT_SOURCE_FILES_PATH, uploaded_file)
        table_name = file_path.split('/')[-1].split('-')[0]
        current_app.logger.info('Running load_paws_data on: ' + uploaded_file)

        df = pd.read_csv((io.BytesIO(open(file_path, "rb").read())), encoding='iso-8859-1')
        current_app.logger.info('   - Populated DF')

        df = __clean_raw_data(df, table_name)
        current_app.logger.info('   - Cleaned DF')

        result[table_name] = pd.DataFrame(columns=["matching_id", "source_type"])
        normalization_without_others = SOURCE_NORMALIZATION_MAPPING[table_name]

        normalization_without_others.pop("others")
        create_normalized_df(df, table_name, normalization_without_others, result)

        current_app.logger.info('   - Finish load_paws_data on: ' + uploaded_file)

    return result

def create_normalized_df(df, table_name, normalization_without_others, result):
    for new_column, table_column in normalization_without_others.items():
        if isinstance(table_column, str):
            result[table_name][new_column] = df[table_column]
        elif callable(table_column):
            result[table_name][new_column] = table_column(df)
        else:
            raise ValueError("Unknown mapping operation")
    current_app.logger.info('   - Normalized DF')
'''
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
'''


def __clean_raw_data(df, table_name):
    # drop the first column - so far all csvs have had a first column that's an index and doesn't have a name
    if DATASOURCE_MAPPING[table_name]["should_drop_first_column"]:
        df = df.drop(df.columns[0], axis=1)

    # strip whitespace and periods from headers, convert to lowercase
    df.columns = df.columns.str.replace(r"\.*\(%\)\.*", "")
    df.columns = df.columns.str.lower().str.strip()
    df.columns = df.columns.map(lambda x: re.sub(r'\s\(.*\)', '', x))
    df.columns = df.columns.str.replace(' ', '_')
    df.columns = df.columns.str.replace('#', 'num')
    df.columns = df.columns.str.replace('/', '_')
    df.columns = df.columns.map(lambda x: re.sub(r'\.+', '_', x))

    return df