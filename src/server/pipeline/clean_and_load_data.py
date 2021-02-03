import pandas as pd
import re
import os
import io
import copy

from datasource_manager import DATASOURCE_MAPPING, SOURCE_NORMALIZATION_MAPPING
from flask import current_app
from config import CURRENT_SOURCE_FILES_PATH


def start(connection, pdp_contacts_df, file_path_list):
    result = pd.DataFrame(columns=pdp_contacts_df.columns)

    for uploaded_file in file_path_list:
        file_path = os.path.join(CURRENT_SOURCE_FILES_PATH, uploaded_file)
        table_name = file_path.split('/')[-1].split('-')[0]
        current_app.logger.info('Running load_paws_data on: ' + uploaded_file)

        df = pd.read_csv((io.BytesIO(open(file_path, "rb").read())), encoding='iso-8859-1')
        current_app.logger.info('   - Populated DF')

        df = __clean_raw_data(df, table_name)
        current_app.logger.info('   - Cleaned DF')

        normalization_without_others = copy.deepcopy(SOURCE_NORMALIZATION_MAPPING[table_name])
        normalization_without_others.pop("others")  # copy avoids modifying the imported mapping

        if "parent" not in normalization_without_others:
            source_df = create_normalized_df(df, normalization_without_others, table_name)

            if result.empty:
                result = source_df
            else:
                result = pd.concat([result, source_df])

        else:
            df.to_sql(table_name, connection, index=False, if_exists='append')

        current_app.logger.info('   - Finish load_paws_data on: ' + uploaded_file)

    return result


def create_normalized_df(df, normalized_df, table_name):
    result = pd.DataFrame(columns=["matching_id"])

    for new_column, table_column in normalized_df.items():
        if isinstance(table_column, str):
            result[new_column] = df[table_column]
        elif callable(table_column):
            result[new_column] = table_column(df)
        else:
            raise ValueError("Unknown mapping operation")
    
    result["source_type"] = table_name
    # Enforce ID datatype to avoid inconsistency when reading/writing table to SQL
    result["source_id"] = result["source_id"].astype(str)

    current_app.logger.info('   - Normalized DF')

    return result




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