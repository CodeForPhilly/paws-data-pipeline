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
MATCH_PRIORITY = ['salesforcecontacts', 'volgistics', 'petpoint']


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


def start(connection, added_or_updated_rows):
    # Match newly identified records to each other and existing master data.

    orig_master = pd.read_sql_table('master', connection)
    input_matches = pd.DataFrame(columns=MATCH_FIELDS)
    input_matches['source'] = []  # also initializing an empty source field, similar to user_info
    master_cols_to_keep = [x for x in MATCH_FIELDS]
    master_cols_to_keep.append('source')
    
    # TODO: handling row updates (possibly)
    # Check consistency of updated_rows
    # If the matching fields (name or email) are updated, then flag the row for human review and processing
    # (e.g. deciding matching when a name changes)
    #for table_name, table_json in added_or_updated_rows['updated_rows'].items():
    #    if len(table_json) == 0:
    #        continue  # empty df, so nothing to do
    #    proposed_updates = pd.DataFrame(table_json)
    # Then, map the proposed update ID back to master table to get the saved user_info name+email
    # Only keep rows where there is a mismatch in name+email. Report these rows in the output dict.
        
    # Match records for new users
    for table_name in MATCH_PRIORITY:
        if table_name not in added_or_updated_rows['new_rows'].keys() or len(added_or_updated_rows['new_rows'][table_name]) == 0:
            continue   # df is empty or not-updated, so there's nothing to do
        
        table_csv_key = _get_table_primary_key(table_name)
        table_master_key = _get_master_primary_key(table_name)
        table_cols = copy.deepcopy(MATCH_FIELDS)
        table_cols.append(table_csv_key)

        # Normalize table and rename columns for compatibility with users
        table_to_match = (
            pd.DataFrame(added_or_updated_rows['new_rows'][table_name])
            .pipe(_reassign_combined_fields, {master_col: DATASOURCE_MAPPING[table_name][table_col] for master_col, table_col in MATCH_MAPPING.items()})
            [table_cols]
            .rename(columns={table_csv_key: table_master_key})
            .pipe(normalize_table_for_comparison, MATCH_FIELDS, orig_prefix='original_')
        )
        orig_compared_cols = ['original_' + col_name for col_name in MATCH_FIELDS]

        input_matches = input_matches.merge(table_to_match, how='outer')
        input_matches['source'].fillna(table_name, inplace=True)
        for col in MATCH_FIELDS:  # also fill untransformed original_cols from source
            if 'source_'+col not in input_matches.columns:
                input_matches['source_'+col] = np.nan
            input_matches['source_'+col].fillna(input_matches['original_'+col], inplace=True)
            del input_matches['original_'+col]
        master_cols_to_keep.append(table_master_key)

    # Resolve new vs. updated records in the master table
    orig_users = pd.read_sql_table('user_info', connection)
    updated_users, new_users, unused_users = join_on_all_columns(
        input_matches,
        normalize_table_for_comparison(orig_users, MATCH_FIELDS)
    )
    # Convert format of new_users -> master_table minus _id column plus name+email_source from user_info
    new_users = (
        new_users
        .drop(columns=MATCH_FIELDS).rename(columns={'source_'+x: x for x in MATCH_FIELDS})
        [master_cols_to_keep]
        .copy()
    )
    # Convert format of updated_users -> master table. Reports the new table_id cols in terms of user_info
    updated_users = (
        updated_users
        [[x for x in updated_users.columns if x.endswith('_id')]]
        .drop(columns='_id')
        .rename(columns={'master_id': '_id'})
    )

    print(new_users.query("name == 'Chris Kohl'").head(10).to_dict(orient='records'))  # Test case, with a known match

    return {
        'new_matches': new_users.to_dict(orient='records'),
        'updated_matches': updated_users.to_dict(orient='records')
    }

