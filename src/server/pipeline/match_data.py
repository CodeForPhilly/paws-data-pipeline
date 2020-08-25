import copy
import pandas as pd
import numpy as np

from fuzzywuzzy import fuzz
from flask import current_app
from datasource_manager import DATASOURCE_MAPPING


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


def normalize_table_for_comparison(df, cols):
    # Standardize specified columns to avoid common/irrelevant sources of mismatching (lowercase, etc)
    out_df = df.copy()
    for column in cols:
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
    # Match newly identified records to each other and existing master data

    # TODO: handling empty json within added_or_updated rows
    # TODO: Log any changes to name or email to a file + visual notification for human review and handling?

    # TODO: check the previous step in the pipeline, that it adds the Names/Emails to Users
    # TODO: how will the names/emails be added to users--who is adding the new row to master?  For now, assume it's already been handled
    # TODO: adding an assertion as such as: assert sum(Users['master_id'].isna()) == 0

    if len(added_or_updated_rows['updated_rows']) > 0:  # any updated rows
        raise NotImplementedError("match_data.start cannot yet handle row updates.")
        # TODO: implement.  Given the new Users workflow, this will likely be just checking if name and email are updated.
        # The only work would be (a) if changed, notify the user since it's hard to automate, or (b) if unchanged, it won't cause a new match.

    orig_master = pd.read_sql_table('master', connection)  #.drop(columns=['created_date', 'archived_date'])
    updated_master = orig_master.copy()
    users_df = pd.read_sql_table('user_info', connection)

    for table_name in MATCH_PRIORITY:
        if table_name not in added_or_updated_rows['new_rows'].keys():
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
            .pipe(lambda df: normalize_table_for_comparison(df, MATCH_FIELDS))
            .rename(columns={table_csv_key: table_master_key})
        )
        # Then get the corresponding rows in master
        table_to_master = (
            table_to_match
            .merge(normalize_table_for_comparison(users_df, MATCH_FIELDS), how='left')
            [[table_master_key, 'master_id']]
        )
        # TODO: save the results of this loop, compile all the tables into master, then return the results to the next step in the flow script.


    # OLD CODE BELOW: finish the code above then delete the rest

    # Combine all of the loaded new_rows into a single dataframe
    new_df = pd.DataFrame({col: [] for col in MATCH_FIELDS})  # init empty dataframe
    for table_name in MATCH_PRIORITY:
        if table_name not in added_or_updated_rows['new_rows'].keys():
            continue  # df is empty or not-updated, so there's nothing to do
            # FIXME: handling empty df here?
        table_csv_key = _get_table_primary_key(table_name)
        table_master_key = _get_master_primary_key(table_name)
        table_cols = copy.deepcopy(MATCH_FIELDS)
        table_cols.append(table_csv_key)

        new_table_data = (
            pd.DataFrame(added_or_updated_rows['new_rows'][table_name])
            .pipe(_reassign_combined_fields, {master_col: DATASOURCE_MAPPING[table_name][table_col] for master_col, table_col in MATCH_MAPPING.items()})
            [table_cols]
            .pipe(lambda df: normalize_table_for_comparison(df, MATCH_FIELDS))
            .rename(columns={table_csv_key: table_master_key})
        )
        new_df = new_df.merge(new_table_data, how='outer')

    # Recreate the normalized MATCH_FIELDS of-record based on the available
    # source data in MATCH_PRIORITY order since not stored in postgres
    master_df = pd.read_sql_table('master', connection).drop(columns=['created_date', 'archived_date'])
    source_dfs = [
        _reassign_combined_fields(
            _get_most_recent_table_records_from_postgres(connection, table),
            {master_col: DATASOURCE_MAPPING[table][table_col] for master_col, table_col in MATCH_MAPPING.items()}
        ).rename(columns={_get_table_primary_key(table): _get_master_primary_key(table)})
        for table in MATCH_PRIORITY
    ]
    master_df = coalesce_fields_by_id(master_df, source_dfs, MATCH_FIELDS)
    master_df = normalize_table_for_comparison(master_df, MATCH_FIELDS)

    # Run the join, then report only the original fields of interest
    matches, left_only, right_only = join_on_all_columns(master_df[MATCH_FIELDS], new_df[MATCH_FIELDS])

    # Use the matching columns (name+email) to handle matching accounting, then drop the ID fields
    new_master_rows = right_only.merge(new_df, how='inner').drop(columns=MATCH_FIELDS)

    # TODO LATER, after getting the new fields working, first.  Also should report the old version of the row.
    # updated_master_rows = coalesce_fields_by_id(
    #    master_df[master_fields],  # TODO: still need to figure out this field
    #    new_df['_temp_new_id' in matches['_temp_new_id']][master_fields]
    # )

    return {'new_matches': new_master_rows.to_dict(orient='records'), 'updated_matches': []}
