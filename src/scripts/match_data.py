import os
import copy

import pandas as pd
import numpy as np

from fuzzywuzzy import fuzz
from config import REPORT_PATH, engine
import datetime

from config import engine
from datasource_manager import DATASOURCE_MAPPING


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
    left_right_indicator='_merge'
    join_results = master_df.merge(table_to_join, indicator=left_right_indicator)
    return (
        join_results[join_results[left_right_indicator]=='left_only'].drop(columns=left_right_indicator),
        join_results[join_results[left_right_indicator]=='right_only'].drop(columns=left_right_indicator),
        join_results[join_results[left_right_indicator]=='both'].drop(columns=left_right_indicator)
    )


def coalesce_fields_by_id(master_table, other_tables, fields):
    # Add fields to master_table from other_tables, in priority order of how they're listed.
    # Similar in intent to running a SQL COALESCE based on the join to each field.
    df_with_updated_fields = master_table.copy()
    df_with_updated_fields[fields] = np.nan
    for table in other_tables:
        # may need to adjust the loop based on the master ID, renaming the fields, depending on how the PK is stored in the volgistics table, etc.
        fields_from_table = master_table.merge(table, how='left', validate='1:1')
        for field_to_update in fields:
            df_with_updated_fields[field_to_update] = df_with_updated_fields[field_to_update].combine_first(fields_from_table[field_to_update])
    return df_with_updated_fields


def normalize_table_for_comparison(df, cols):
    # Standardize cpecified columns to avoid common/irrelevant sources of mismatching (lowercase, etc)
    out_df = df.copy()
    for column in cols:
        out_df[column] = out_df[column].str.strip().str.lower()
    return out_df


# Big questions/TODOs
# 1. When is master_df initialized?
# 2. What schema will master_df take?  petpoint_id, salesforcecontacts_id, etc.?
# 3. Can we include the name/email of-record in master_df to simplify matching?
#    If not, the matching script will need to recreate these values and do some extra accounting to match everything back.
# 4. Note: load_paws_data.__find_updated_rows is still using the old deleted_date notation
# 5. Log any changes to name or email to a file + visual notification for human review and handling?
# 6. Adjusting the stubs and code assumptions below, according to decisions about these questions


### STUBS TO IMPLEMENT OR FIGURE OUT ###
def _get_master_df():
    # FIXME: stub which should be replaced by load_paws_data, create_master_df, or another database-aware file
    # Gets the full master dataframe from postgres so we can identify new vs. old matches
    return pd.DataFrame(columns=['email', 'name', 'salesforcecontacts_id', 'volgistics_id', 'petpoint_id'])

def _get_most_recent_table_records_from_postgres(table_name):
    select_query = f'select * from {table_name} where archived_date is null'
    #with engine.connect() as conn:
    #    rows = conn.execute(select_query)
    return pd.read_sql(select_query, engine)

def _get_table_primary_key(source_name):
    return DATASOURCE_MAPPING[source_name]['id']

def _get_master_primary_key(source_name):
    # NOTE: may change based on the decisions for how master_df is structured
    return source_name + '_id'

def start(added_or_updated_rows):
    # Match newly identified records to each other and existing master data
    # FIXME: not yet operational: see function stubs below to refactor

    # TODO: Still need to replace a few functions that have placeholder names:
    # Define _get_most_recent_table_records_from_postgres with help from Steve to extract the new names (SELECT * FROM X WHERE _MOST_RECENT)
    # def _get_primary_key(source_name): return source_name+'_id' (?)
    # FIXME: added_or_updated_rows json has an irregular tuple input format instead of key:value or similar

    # TODO: cleaning up the comments above and throughout
    # TODO: handling empty json within added_or_updated rows

    if len(added_or_updated_rows['updated_rows']) > 0:  # any updated rows
        raise NotImplementedError("match_data.start cannot yet handle row updates.")

    # Matching columns and table order priority as established by
    # https://github.com/CodeForPhilly/paws-data-pipeline/blob/master/documentation/matching_rules.md
    # TODO: refactor out into a settings import from ../datasource_manager.py
    match_criteria = ['email', 'name']
    table_mapping = {
        #'salesforcecontacts': {'full_name': 'name', 'email': 'email'},
        #'volgistics': {'full_name': 'name', 'email': 'email'},
        #'petpoint': {'outcome_person_name': 'name', 'out_email': 'email'}
        'salesforcecontacts': {'email': 'email', 'name': ['first_name', 'last_name']},
        'volgistics': {'email': 'email', 'name': ['first_name', 'last_name']},
        'petpoint': {'email': 'out_email', 'name': ['outcome_person_name']}
    }
    table_priority = ['salesforcecontacts', 'volgistics', 'petpoint']

    # Recreate the normalized match_criteria of-record based on the available source data based on the table_priority order
    master_df = _get_master_df()  # FIXME: does this table even exist in the load_paws_data.py or before the matching script is called?
    master_fields = master_df.columns
    #master_df = coalesce_fields_by_id(  # no longer necessary if name+email is in master_df
    #    master_df,
    #    [_get_most_recent_table_records_from_postgres(x) for x in table_priority],
    #    match_criteria
    #)
    master_df = normalize_table_for_comparison(master_df, match_criteria)

    # Combine all of the loaded new_rows into a single dataframe
    new_df = pd.DataFrame({col: [] for col in match_criteria})  # init an empty dataframe to collect the new data in one place
    for table_name in table_priority:
        if table_name not in added_or_updated_rows['new_rows'].keys():
            continue  # df is empty or not-updated, so there's nothing to do
            # FIXME: handling empty df here?
        table_csv_key = _get_table_primary_key(table_name)
        table_master_key = _get_master_primary_key(table_name)
        table_cols = copy.deepcopy(match_criteria)
        table_cols.append(table_csv_key)
        def combine_names(df, fields, sep=' '):
            if len(fields) == 1:
                return df[fields[0]]
            else:
                return df[fields[0]].str.cat(others=df[fields[1:]], sep=sep)
        new_table_data = (
            pd.DataFrame(added_or_updated_rows['new_rows'][table_name])
            .rename(columns={table_mapping[table_name]['email']: 'email'})
            .assign(name=lambda df: combine_names(df, table_mapping[table_name]['name']))
            [table_cols]
            .pipe(lambda df: normalize_table_for_comparison(df, match_criteria))
            .rename(columns={table_csv_key: table_master_key})
        )
        new_df = new_df.merge(new_table_data, how='outer')

    # Run the join, then report only the original fields of interest
    matches, left_only, right_only = join_on_all_columns(master_df[match_criteria], new_df[match_criteria])
    #new_master_rows = new_df[new_df['_temp_new_id'] in right_only['_temp_new_id']][master_fields]
    new_master_rows = right_only.merge(new_df, how='inner')  # associate name+email back to the IDs
    # TODO LATER, after getting the new fields working, first.  Also should report the old version of the row.
    #updated_master_rows = coalesce_fields_by_id(
    #    master_df[master_fields],  # TODO: still need to figure out this field
    #    new_df['_temp_new_id' in matches['_temp_new_id']][master_fields]
    #)

    return {'new_matches': new_master_rows.to_dict(), 'updated_matches': ['empty_for_now']}
