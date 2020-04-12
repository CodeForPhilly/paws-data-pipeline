import sqlite3
import pandas as pd
import os
import sys

from fuzzywuzzy import fuzz

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from scripts.load_paws_data import OUTPUT_PATH

LOG_PATH = os.path.join(OUTPUT_PATH, 'logs/')
TRANSFORM_EMAIL_NAME = 'lower_email'
MATCH_COLUMNS_TO_KEEP=['table_id', TRANSFORM_EMAIL_NAME, 'table_name']


def single_fuzzy_score(record1, record2):
    # Calculate a fuzzy matching score between two strings.
    # Uses a modified Levenshtein distance from the fuzzywuzzy package.
    # Update this function if a new fuzzy matching algorithm is selected.
    # Similar to the example of "New York Yankees" vs. "Yankees" in the documentation, we 
    # should use fuzz.partial_ratio instead of fuzz.ratio to more gracefully handle nicknames.
    # https://chairnerd.seatgeek.com/fuzzywuzzy-fuzzy-string-matching-in-python/
    return fuzz.partial_ratio(record1, record2)


def df_fuzzy_score(df, column1_name, column2_name):
    # Calculates a new column of fuzzy scores from two columns of strings.
    # Slow in part due to a nonvectorized loop over rows
    return df.apply(lambda row: single_fuzzy_score(row[column1_name], row[column2_name]), axis=1)


class MismatchLogger:
    def __init__(self, reason_column='error_reason'):
        self.errors = pd.DataFrame()
        self.reason_column = reason_column
        
    def log_rows(self, error_df, reason_code='Reason not specified'):
        error_with_reason = error_df.copy()
        error_with_reason[self.reason_column] = reason_code
        self.errors = self.errors.append(error_with_reason)
    
    def write_log(self, file_basename, dir=LOG_PATH):
        # Currently writing to a csv, but we could also consider a DB table
        # convention for logging, e.g. log_mismatch_salesforce_and_volgistics
        self.errors.to_csv(os.path.join(dir, file_basename), index=False)


def read_from_sqlite(table_name):
    # Extracting pandas tables out from load_paws_data.load_to_sqlite
    connection = sqlite3.connect(os.path.join(OUTPUT_PATH, "paws.db"))
    df = pd.read_sql_query("SELECT * FROM ?;", connection, params=(table_name))
    connection.close()
    return df


def remove_duplicates(df, field):
    duplicate_ids = df.groupby(field).count().reset_index().query("table_id > 1")[field]
    #volgistics[volgistics['lower_email'].isin(duplicate_volgistics_emails['lower_email'])]
    unique_rows = df[~df[field].isin(duplicate_ids)]
    duplicate_rows = df[df[field].isin(duplicate_ids)]
    return (unique_rows, duplicate_rows)


def remove_null_rows(df, field):
    nonnull_rows = df[~df[field].isnull()]
    null_rows = df[df[field].isnull()]
    return (nonnull_rows, null_rows)


def cleanup_and_log_table(df, important_fields, log_name='mismatches.csv'):
    cleaned_df = df.copy()
    for renamed, orig in important_fields.items():
        if renamed.startswith('_'):
            continue
        cleaned_df[renamed] = cleaned_df[orig]
    
    # Reconstructing names, allowing for it to be split across multiple fields
    cleaned_df['table_name'] = cleaned_df[important_fields['_table_name'][0]]
    for i in range(1, len(important_fields['_table_name'])):
        cleaned_df['table_name'] = cleaned_df['table_name'] + ' ' + cleaned_df['_table_name'][i]
    
    # Applying a lowercase filter to email for matching purposes, since the case is usually
    # inconsistent, and logging potential issues for matching (as well as duplicate/null ID's,
    # which would also be unexpected in a clean data source)
    cleaned_df[TRANSFORM_EMAIL_NAME] == cleaned_df['table_email'].str.lower()
    mismatches = MismatchLogger()
    for cleanup_field in [TRANSFORM_EMAIL_NAME, 'table_id']:
        cleaned_df, null_df = remove_null_rows(cleaned_df, cleanup_field)
        mismatches.log_rows(null_df, 'Null {}'.format(cleanup_field))
        cleaned_df, duplicate_df = remove_duplicates(df, cleanup_field)
        mismatches.log_rows(duplicate_df, 'Multiple {}'.format(cleanup_field))
    mismatches.write_log(log_name)

    return cleaned_df


def match_by_field(master_df, other_df, output_ids=['master_id', 'other_id'], match_field=TRANSFORM_EMAIL_NAME, id_field='table_id'):
    master_cols = master_df[[id_field, match_field]].rename(columns={id_field: output_ids[0]})
    other_cols = other_df[[id_field, match_field]].rename(columns={id_field: output_ids[1]})
    matches = master_cols.merge(other_cols, how='inner')
    
    matched_vals = matches[match_field]
    unmatched_master = master_cols[~master_cols[match_field].isin(matched_vals)]
    unmatched_other = other_cols[~other_cols[match_field].isin(matched_vals)]
    return (matches, unmatched_master, unmatched_other)


def match_cleaned_table(salesforce_df, table_df, table_name, log_name='unmatched.csv'):
    salesforce_id_field = 'salesforce_id'
    table_id_field = table_name + '_id'
    salesforce_name_field = 'salesforce_name'
    table_name_field = table_name + '_name'

    # Match by email
    matched, unmatched_salesforce, unmatched_table = match_by_field(
        salesforce_df[MATCH_COLUMNS_TO_KEEP].rename(columns={'table_name': salesforce_name_field}),
        table_df[MATCH_COLUMNS_TO_KEEP].rename(columns={'table_name': table_name_field}),
        output_id=[salesforce_id_field, table_id_field],
        match_field=TRANSFORM_EMAIL_NAME,
        id_field='table_id'
    )
    # Apply fuzzy matching on names
    matched['name_fuzzy_score'] = df_fuzzy_score(matched, table_name_field, salesforce_name_field)
    unmatched_by_name = matched[matched['fuzzy_name_score'] != 100].copy()
    matched = matched[matched['fuzzy_name_score'] == 100]

    # TODO: ANY OTHER MATCH DOCUMENTATION TO ADD OR MODIFY FROM MEG, CHRIS, AND KARLA?

    # Log mismatches from the new table
    mismatches = MismatchLogger()
    mismatches.log_rows(unmatched_table, 'Email not found in Salesforce')
    mismatches.log_rows(unmatched_by_name, 'Name did not match Salesforce')
    mismatches.write_log(log_name)

    return matched

