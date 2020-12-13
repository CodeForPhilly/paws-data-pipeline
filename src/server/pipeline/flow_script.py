import os

from pipeline import load_paws_data, match_data, create_master_df, clean_and_load_data
from config import CURRENT_SOURCE_FILES_PATH
from config import engine
from models import Base


def start_flow():
    file_path_list = os.listdir(CURRENT_SOURCE_FILES_PATH)

    if file_path_list:
        with engine.connect() as connection:
            Base.metadata.create_all(connection)

            # Clean the input data and normalize
            # input - existing files in path
            # output - normalized object of all entries
            normalized_data = clean_and_load_data.start(connection, file_path_list)

            # todo: load existing pdp contact table into a dataframe
            # todo: compare two dataframes
            #       1. drop existing data and keep updated and new entries

            # todo: Split object from previous step to new items and updated. drop existing items
            # STEP
            rows_to_add_or_updated = load_paws_data.start(normalized_data)

            # todo: Remove renaming
            # todo: Run fuzzy match on all new and updated items
            # todo: When match found - generate matching ID and add to both matching columns (if there is one use it)
            rows_for_master_df = match_data.start(connection, rows_to_add_or_updated)

            # load to pdp_contacts DB
            create_master_df.start(connection, rows_for_master_df)
