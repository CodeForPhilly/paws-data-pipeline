import pandas as pd
import os

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
    # FIXME: added_or_updated_rows json has an irregular tuple input format instead of key:value or similar

    # TODO: implement updated_rows
    if len(added_or_updated_rows['updated_rows']) > 0:  # any updated rows
        raise NotImplementedError("match_data.start cannot yet handle row updates.")

    # Matching columns and table order priority as established by
    # https://github.com/CodeForPhilly/paws-data-pipeline/blob/master/documentation/matching_rules.md
    # TODO: refactor out into a settings import, likely in the same place where the table names and keys are defined
    match_criteria = ['email', 'name']
    table_priority = ['salesforcecontacts', 'volgistics', 'petpoint', 'ClinicHQ']
    
    # Append fields from the source tables (Salesforce, volgistics, petpoint, etc.) in priority order, then normalize
    master_df = coalesce_fields_by_id(
        _get_master_df(),
        [_get_most_recent_table_records_from_postgres(x) for x in table_priority],  # pseudo code
        match_criteria
    )
    master_df = normalize_table_for_comparison(master_df, match_criteria)

    updated_master_rows = pd.DataFrame()
    new_master_rows = pd.DataFrame()
    # TODO: need to attempt to match the new rows first to each other, then to the master table, or
    # come up with another logic to reconcile updates to multiple columns simultaneously (or how to represent those cases)
    # e.g. Formerly salesforce-only now also has volgistics and petpoint keys.
    # Also, how to handle which columns are being passed in the table normalization here???
    for table_name in table_priority:
        if table_name not in input_data['new_rows'].keys():
            continue  # df is empty or not-updated, so there's nothing to do
        new_table_data = normalize_table_for_comparison(pd.DataFrame(input_data['new_rows'][table_name]))
        
        matches, left_only, right_only = join_on_all_columns(master_df, new_table_data)
        updated_master_rows = updated_master_rows.append(matches)
        new_master_rows = new_master_rows.append(right_only)
        master_df = matches.append(left_only).append(right_only)
    return {'new_matches': new_master_rows.to_dict(), 'updated_matches': updated_master_rows.to_dict()}
