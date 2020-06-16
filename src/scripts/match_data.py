import pandas as pd
import os
import copy

from fuzzywuzzy import fuzz
from config import REPORT_PATH, engine
import datetime


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


def start(added_or_updated_rows):
    # Match newly identified records to each other and existing master data
    # FIXME: not yet operational: see function stubs below to refactor

    # TODO: Still need to replace a few functions that have placeholder names:
    # Define _get_most_recent_table_records_from_postgres with help from Steve to extract the new names (SELECT * FROM X WHERE _MOST_RECENT)
    # _get_master_df to get the full master dataframe from postgres, and load in the data to match against historical data
    # def _get_primary_key(source_name): return source_name+'_id' (?)
    # FIXME: added_or_updated_rows json has an irregular tuple input format instead of key:value or similar

    if len(added_or_updated_rows['updated_rows']) > 0:  # any updated rows
        raise NotImplementedError("match_data.start cannot yet handle row updates.")

    # Matching columns and table order priority as established by
    # https://github.com/CodeForPhilly/paws-data-pipeline/blob/master/documentation/matching_rules.md
    # TODO: refactor out into a settings import, likely in the same place where the table names and keys are defined
    match_criteria = ['email', 'name']
    table_priority = ['salesforcecontacts', 'volgistics', 'petpoint', 'ClinicHQ']

    # Recreate the normalized match_criteria of-record based on the available source data based on the table_priority order
    master_df = _get_master_df()
    master_fields = master_df.columns
    master_df = coalesce_fields_by_id(
        master_df,
        [_get_most_recent_table_records_from_postgres(x) for x in table_priority],
        match_criteria
    )
    master_df = normalize_table_for_comparison(master_df, match_criteria)

    # Summarize all of the new_rows from the previous step into a single dataframe of changes
    new_df = pd.DataFrame({col: [] for col in match_criteria})  # init an empty dataframe to collect the new data in one place
    for table_name in table_priority:
        if table_name not in input_data['new_rows'].keys():
            continue  # df is empty or not-updated, so there's nothing to do
        table_cols = copy.deepcopy(match_criteria)
        table_cols.append(_get_primary_key(table_name))
        new_table_data = normalize_table_for_comparison(pd.DataFrame(input_data['new_rows'][table_name]))[table_cols]
        new_df = new_df.merge(new_table_data, how='outer')

    # Run the join, then report only the original fields of interest
    master_df['_temp_orig_id'] = np.arange(master_df.shape[0] + 1)
    master_df_matching_cols = copy.deepcopy(match_criteria)
    master_df_matching_cols.append('_temp_orig_id')
    new_df['_temp_new_id'] = np.arange(new_df.shape[0] + 1)
    new_df_matching_cols = copy.deepcopy(match_criteria)
    new_df_matching_cols.append('_temp_new_id')

    matches, left_only, right_only = join_on_all_columns(master_df[master_df_matching_cols], new_df[new_df_matching_cols])
    new_master_rows = new_df[new_df['_temp_new_id'] in right_only['_temp_new_id']][master_fields]
    updated_master_rows = new_df['_temp_new_id' in matches['_temp_new_id']][master_fields]
    # and could get the former versions of those rows via a similar merge step or filter for master_df

    return {'new_matches': new_master_rows.to_dict(), 'updated_matches': updated_master_rows.to_dict()}
