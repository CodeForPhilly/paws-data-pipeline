import datetime, time
import pandas as pd
import numpy as np
from sqlalchemy.sql import text
import re

from flask import current_app
from pipeline import log_db


def normalize_before_match(value):
    result = None

    if isinstance(value, str):
        result = value.lower().replace('"', '')

    return result
    

def start(connection, added_or_updated_rows, manual_matches_df, job_id):
    # Match new records to each other and existing pdp_contacts data.
    # Assigns matching ID's to records, as well.
    # WARNING: not thread-safe and could lead to concurrency issues if two users /execute simultaneously
    current_app.logger.info('Start record matching')
    # Will need to consider updating the existing row contents (filter by active), deactivate,
    # try to match, and merge previous matching groups if applicable
    # job_id = str(int(time.time()))
    log_db.log_exec_status(job_id, 'matching', 'executing', '')

    current_app.logger.info("***** Running execute job ID " + job_id + " *****")
    items_to_update = pd.concat([added_or_updated_rows["new"], added_or_updated_rows["updated"]], ignore_index=True)

    query = "select max(matching_id) as matching_id from pdp_contacts where archived_date is null"
    max_matching_id = connection.execute(query).fetchone()[0]
    if max_matching_id == None:
        max_matching_id = 0
        
    # Initialize column metadata we'll write to pdp_contacts
    items_to_update["matching_id"] = 0  # initializing an int and overwrite in the loop
    items_to_update["archived_date"] = np.nan
    items_to_update["created_date"] = datetime.datetime.now()

    # Create Normalized columns for matching
    items_to_update["first_name_normalized"] = items_to_update["first_name"].apply(normalize_before_match)
    items_to_update["last_name_normalized"] = items_to_update["last_name"].apply(normalize_before_match)
    items_to_update["email_normalized"] = items_to_update["email"].apply(normalize_before_match)

    rows = items_to_update.to_dict(orient="records")
    row_print_freq = 1000 

    for row_num, row in enumerate(rows):
        if row_num % row_print_freq == 0:
            current_app.logger.info("- Matching rows {}-{} of {}".format(
                row_num + 1, min(len(rows), row_num + row_print_freq), len(rows))
            )
            log_db.log_exec_status(job_id, 'matching', 'executing', str({'at_row': row_num + 1, 'of_rows': len(rows)  }) )

        # Exact matches based on specified columns
        query = text("""select matching_id from pdp_contacts where archived_date is null and ( 
                ( 
	                (((string_to_array(lower(first_name), ',') && :first_name) and (string_to_array(lower(last_name), ',') && :last_name)) 
	                or 
	                ((string_to_array(lower(first_name), ',') && :last_name) and (string_to_array(lower(last_name), ',') && :first_name))) 
                    and 
                    (lower(email) = :email or mobile = :mobile) 
                ))""")
        
        #TODO revist name tokenization
        delimiters = ' and | & |, | '
        first_name_tokenized = re.split(delimiters, row["first_name_normalized"]) if row["first_name_normalized"] is not None else []
        last_name_tokenized = re.split(delimiters, row["last_name_normalized"]) if row["last_name_normalized"] is not None else []
        
        results = connection.execute(query, first_name=first_name_tokenized, last_name=last_name_tokenized, email=row["email_normalized"], mobile=row["mobile"])
        existing_ids = list(map(lambda x: x.matching_id, results.fetchall()))
        
        #collect other linked ids from manual matches source
        if not manual_matches_df.empty:
            linked_ids = manual_matches_df[(manual_matches_df[row["source_type"]] == row["source_type"])]
            ids = linked_ids.to_dict(orient="records")
            for id_num, row_dict in enumerate(ids):
                for column, value in row_dict.items():
                    query = "select matching_id from pdp_contacts where source_type = :source_type and and source_id = :source_id and archived date is null"
                    results = connection.execute(query, source_type=column, source_id=value)
                    #TODO log ids provided by manual matches and not part of auto-matching
                    existing_ids = existing_ids + list(map(lambda x: x.matching_id, results.fetchall()))
        
        if len(existing_ids) == 0:
            max_matching_id += 1
            matching_id = max_matching_id
        else:
            matching_id = max(existing_ids)
            same_id = all(id == existing_ids[0] for id in existing_ids)
            if not same_id:
                old_ids = [id for id in existing_ids if id != matching_id]
                for old_id in old_ids:
                    query = text("update pdp_contacts set matching_id = :matching_id where matching_id = :old_id and archived_date is null")
                    connection.execute(query, matching_id=matching_id, old_id=old_id) 
                    current_app.logger.info("glue record found, changing id {} to {}".format(old_id, matching_id))
        
        insert = text("insert into pdp_contacts(matching_id, source_type, source_id, first_name, last_name, email, mobile, street_and_number, apartment, city, state, zip) \
                    values(:matching_id, :source_type, :source_id, :first_name, :last_name, :email, :mobile, :street_and_number, :apartment, :city, :state, :zip)")
        connection.execute(insert, matching_id=matching_id, source_type=row["source_type"], source_id=row["source_id"], first_name=row["first_name"], last_name=row["last_name"], email=row["email"], mobile=row["mobile"], street_and_number=row["street_and_number"], apartment=row["apartment"], city=row["city"], state=row["state"], zip=row["zip"])
    
    current_app.logger.info("- Finished load to pdp_contacts table")
    log_db.log_exec_status(job_id, 'matching', 'executing', str({'at_row': len(rows), 'of_rows': len(rows) }) )
