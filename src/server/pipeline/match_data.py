import datetime
import pandas as pd
import numpy as np

from flask import current_app


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

    # Initialize column metadata we'll write to pdp_contacts
    items_to_update["matching_id"] = 0  # initializing an int and overwrite in the loop
    items_to_update["archived_date"] = np.nan
    items_to_update["created_date"] = datetime.datetime.now()
    if "_id" in items_to_update.columns:
        del row["_id"]  # avoid specifying the _id field, so postgres will auto-increment for us
    
    rows = items_to_update.to_dict(orient="records")
    for row_num, row in enumerate(rows):
        current_app.logger.info("- Matching row {} of {}".format(row_num+1, len(rows)))
        # Exact matches based on specified columns
        row_matches = pdp_contacts[
            (pdp_contacts["first_name"] == row["first_name"]) &
            (pdp_contacts["last_name"] == row["last_name"]) &
            (pdp_contacts["email"] == row["email"]) # TODO: could transform this line into an "or" with phone number
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
        items_to_update["matching_id"][row_num] = row_group
        # Updating local pdp_contacts dataframe instead of a roundtrip to postgres within the loop.
        # Indexing by iloc and vector of rows to keep the pd.DataFrame class and avoid implicit
        # casting to a single-typed pd.Series.
        pdp_contacts = pdp_contacts.append(items_to_update.iloc[[row_num], :])
    
    # Write new data and matching ID's to postgres in bulk, instead of line-by-line
    items_to_update.to_sql('pdp_contacts', connection, index=False, if_exists='append')
