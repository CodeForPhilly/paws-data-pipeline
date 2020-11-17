import os

from pipeline import load_paws_data, match_data, create_master_df, init_db_schema
from config import CURRENT_SOURCE_FILES_PATH
from config import engine


def start_flow():
    file_path_list = os.listdir(CURRENT_SOURCE_FILES_PATH)

    if file_path_list:
        with engine.connect() as connection:
            init_db_schema.start(connection)

            rows_to_add_or_updated = load_paws_data.start(connection, file_path_list)

            rows_for_master_df = match_data.start(connection, rows_to_add_or_updated)

            create_master_df.start(connection, rows_for_master_df)
