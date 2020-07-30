import os

from scripts import load_paws_data, match_data, create_master_df, init_db_schema
from config import CURRENT_SOURCE_FILES_PATH


def start_flow():
    file_path_list = os.listdir(CURRENT_SOURCE_FILES_PATH)

    if file_path_list:
        init_db_schema.start()

        rows_to_add_or_updated = load_paws_data.start(file_path_list, True)

        rows_for_master_df = match_data.start(rows_to_add_or_updated)

        create_master_df.start(rows_for_master_df)
