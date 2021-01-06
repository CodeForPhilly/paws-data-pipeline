import copy
import pandas as pd
import numpy as np

from fuzzywuzzy import fuzz
from flask import current_app

from datasource_manager import DATASOURCE_MAPPING
from pipeline.create_master_df import __create_new_user


# Matching columns and table order priority as established by
# https://github.com/CodeForPhilly/paws-data-pipeline/blob/master/documentation/matching_rules.md
MATCH_MAPPING = {'email': 'table_email', 'name': '_table_name'}
MATCH_FIELDS = list(MATCH_MAPPING.keys())
MATCH_PRIORITY = ['salesforcecontacts', 'volgistics', 'shelterluvpeople']


def single_fuzzy_score(record1, record2, case_sensitive=False):
    # Calculate a fuzzy matching score between two strings.
    # Uses a modified Levenshtein distance from the fuzzywuzzy package.
    # Update this function if a new fuzzy matching algorithm is selected.
    # Similar to the example of "New York Yankees" vs. "Yankees" in the documentation, we 
    # should use fuzz.partial_ratio instead of fuzz.ratio to more gracefully handle nicknames.
    # https://chairnerd.seatgeek.com/fuzzywuzzy-fuzzy-string-matching-in-python/
    if not case_sensitive:
        record1 = record1.lower()
        record2 = record2.lower()
    return fuzz.partial_ratio(record1, record2)


def df_fuzzy_score(df, column1_name, column2_name, **kwargs):
    # Calculates a new column of fuzzy scores from two columns of strings.
    # Slow in part due to a nonvectorized loop over rows
    if df.empty:
        return []
    else:
        return df.apply(lambda row: single_fuzzy_score(row[column1_name], row[column2_name], **kwargs), axis=1)


def join_on_all_columns(master_df, table_to_join):
    # attempts to join based on all columns
    left_right_indicator = '_merge'
    join_results = master_df.merge(table_to_join, how='outer', indicator=left_right_indicator)
    return (
        join_results[join_results[left_right_indicator] == 'both'].drop(columns=left_right_indicator),
        join_results[join_results[left_right_indicator] == 'left_only'].drop(columns=left_right_indicator),
        join_results[join_results[left_right_indicator] == 'right_only'].drop(columns=left_right_indicator)
    )


def normalize_table_for_comparison(df, cols, orig_prefix=None):
    # Standardize specified columns to avoid common/irrelevant sources of mismatching (lowercase, etc)
    out_df = df.copy()
    for column in cols:
        if orig_prefix is not None:
            out_df[orig_prefix+column] = out_df[column]
        # NOTE: make sure this regex is correct
        out_df[column] = out_df[column].astype(str).str.strip().str.lower().str.replace("[^a-z0-9]", "")
    return out_df


def combine_fields(df, fields, sep=' '):
    if isinstance(fields, str):
        return df[fields]
    else:
        assert isinstance(fields, list)
    if len(fields) == 1:
        return df[fields[0]]
    else:
        return df[fields[0]].str.cat(others=df[fields[1:]], sep=sep)


def _reassign_combined_fields(df, field_mapping):
    out_df = df.copy()
    for new_field, old_field in field_mapping.items():
        out_df[new_field] = combine_fields(out_df, old_field)
    return out_df


def _get_most_recent_table_records_from_postgres(connection, table_name):
    select_query = f'select * from {table_name} where archived_date is null'
    return pd.read_sql(select_query, connection)


def _get_table_primary_key(source_name):
    return DATASOURCE_MAPPING[source_name]['id']


def _get_master_primary_key(source_name):
    return source_name + '_id'


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
    pdp_contacts = pd.read_sql_table('pdp_contacts', connection)

    if pdp_contacts.shape[0] == 0:
        max_matching_group = 0
    else:
        max_matching_group = max(pdp_contacts["matching_id"]) + 1

    # todo: concat new and updated to iterate
    #items_to_update = added_or_updated_rows["new"] + added_or_updated_rows["updated"]

    for index, row in added_or_updated_rows["new"].iterrows():
        # Exact matches based on specified columns
        # Replacing: row[["first_name", "last_name", "email"]].merge(pdp_contacts, how="inner")
        row_matches = pdp_contacts[
            (pdp_contacts["first_name"] == row["first_name"]) &
            (pdp_contacts["last_name"] == row["last_name"]) &
            (pdp_contacts["email"] == row["email"])
        ]
        if row_matches.shape[0] == 0:  # new record, no matches
            row_group = max_matching_group
            max_matching_group += 1
        else:  # existing match(es)
            row_group = row_matches["matching_id"].values[0]
            if not all(row_matches["matching_id"] == row_group):
                current_app.logger.warning(
                    "Source {} with ID {} is matching multiple groups in pdp_contacts ({})"
                    .format(row["source_type"], row["source_id"], str(row_matches["matching_id"].drop_duplicates()))
                )
        row["created_at"] = "TODO NOW"
        row["archived_at"] = np.nan
        row["matching_id"] = row_group

        # todo: fix load to sql - try row.toFrame
        pd.DataFrame(row).to_sql('pdp_contacts', connection, index=False, if_exists='append')
        pdp_contacts = pd.read_sql_table('pdp_contacts', connection)
