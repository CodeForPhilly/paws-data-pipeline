import os

from pipeline import load_paws_data, match_data, create_master_df
from config import CURRENT_SOURCE_FILES_PATH
from config import engine
from models import Base


def start_flow():
    file_path_list = os.listdir(CURRENT_SOURCE_FILES_PATH)

    if file_path_list:
        with engine.connect() as connection:
            Base.metadata.create_all(connection)

            # todo: Clean the input data and Create an object of new rows and rows to update
            rows_to_add_or_updated = load_paws_data.start(connection, file_path_list)

            # todo: add normalization step to create one big object that follows the schema
            #STEP

            # todo: Remove renaming
            # todo: Run fuzzy match on all new and updated items
            # todo: When match found - generate matching ID and add to both matching columns (if there is one use it)
            rows_for_master_df = match_data.start(connection, rows_to_add_or_updated)

            # load to pdp_contacts DB
            create_master_df.start(connection, rows_for_master_df)
