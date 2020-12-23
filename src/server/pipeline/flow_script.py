import os
import pandas as pd
from pipeline import calssify_new_data,clean_and_load_data
from config import CURRENT_SOURCE_FILES_PATH
from config import engine
from models import Base


def start_flow():
    file_path_list = os.listdir(CURRENT_SOURCE_FILES_PATH)

    if file_path_list:
        with engine.connect() as connection:
            Base.metadata.create_all(connection)

            pdp_contacts_df = pd.read_sql_table('pdp_contacts', connection)

            # Clean the input data and normalize
            # input - existing files in path
            # output - normalized object of all entries
            normalized_data = clean_and_load_data.start(pdp_contacts_df, file_path_list)

            # todo: Split object from previous step to new items and updated. drop existing items
            # todo: A good place to consider archiving items that were updated
            # STEP
            rows_to_add_or_updated = calssify_new_data.start(pdp_contacts_df, normalized_data)

            # todo: Remove renaming
            # todo: Run fuzzy match on all new and updated items
            # todo: When match found - generate matching ID and add to both matching columns (if there is one use it)

            # match and load:
            # for each item
                ### if it matches - it will get the same matching id as the match
                ### if it doesn't - generate matching id (some prefix with increment?)
                ### new item:
                    ### load it with created_at = now and archived_at = null
                ### updated item:
                    ### can we just use everything as new item if we are already archiving?



            ## test::
            rows_to_add_or_updated["new"].to_sql('pdp_contacts', connection, index=False, if_exists='append')

            print(1)
            # rows_for_master_df = match_data.start(connection, rows_to_add_or_updated)

            # load to pdp_contacts DB
            # create_master_df.start(connection, rows_for_master_df)
