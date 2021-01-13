import datetime
import pandas as pd
import numpy as np

from flask import current_app


# todo: match and load
#   Compare each new and updated item to all records in the DB
#   (including all other items that are new and updated this iteration) - for each item:
#       if it matches - it will get the same matching id as the match
#       if it doesn't - generate matching id (some prefix with increment?)
#       load it with created_at = now and archived_at = null

def start(connection, added_or_updated_rows):
    # Match new records to each other and existing pdp_contacts data.
    # Assigns matching ID's to records, as well.
    # WARNING: not thread-safe and could lead to concurrency issues if two users /execute simultaneously
    current_app.logger.info('Start record matching')
    current_app.logger.warning('Matching updated records not yet handled')
    # Will need to consider updating the existing row contents (filter by active), deactivate,
    # try to match, and merge previous matching groups if applicable
    items_to_update = pd.concat([added_or_updated_rows["new"], added_or_updated_rows["updated"]], ignore_index=True)
    pdp_contacts = pd.read_sql_table('pdp_contacts', connection)

    if pdp_contacts["matching_id"].dropna().size == 0:
        max_matching_group = 0
    else:
        max_matching_group = max(pdp_contacts["matching_id"].dropna()) + 1

    # Iterate over the dataframe using integer index location,
    # because iterrows returns a type-inconsistent series, and itertuples would be more complex.
    num_added_or_updated = items_to_update.shape[0]
    for row_num in range(num_added_or_updated):
        current_app.logger.info("- Matching row {} of {}".format(row_num+1, num_added_or_updated))
        row = items_to_update.iloc[[row_num], :].copy()  # pd.DataFrame
        # Exact matches based on specified columns
        row_matches = pdp_contacts[
            (pdp_contacts["first_name"] == row["first_name"].values[0]) &
            (pdp_contacts["last_name"] == row["last_name"].values[0]) &
            (pdp_contacts["email"] == row["email"].values[0])
        ]
        if row_matches.shape[0] == 0:  # new record, no matching rows
            row_group = max_matching_group
            max_matching_group += 1
        else:  # existing match(es)
            row_group = row_matches["matching_id"].values[0]
            if not all(row_matches["matching_id"] == row_group):
                current_app.logger.warning(
                    "Source {} with ID {} is matching multiple groups in pdp_contacts ({})"
                    .format(row["source_type"], row["source_id"], str(row_matches["matching_id"].drop_duplicates()))
                )
        row["created_date"] = datetime.datetime.now()
        row["archived_date"] = np.nan
        row["matching_id"] = row_group
        if "_id" in row.columns:
            del row["_id"]  # avoid specifying the _id field, so postgres will auto-increment for us

        # Round-trip to the database on every loop iteration is inefficient and could be rewritten much faster
        row.to_sql('pdp_contacts', connection, index=False, if_exists='append')
        pdp_contacts = pd.read_sql_table('pdp_contacts', connection)
