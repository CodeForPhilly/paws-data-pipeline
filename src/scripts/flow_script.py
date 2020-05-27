import os
import pandas as pd

from scripts import load_paws_data, match_data, create_master_df
from config import CURRENT_SOURCE_FILES_PATH, LOGS_PATH, engine
from flask import current_app

MAPPING_FIELDS = {
    'salesforcecontacts': {
        '_label': 'salesforce',
        'table_id': 'contact_id',
        'table_email': 'email',
        '_table_name': ['first_name', 'last_name']
    },
    'petpoint': {
        '_label': 'petpoint',
        'table_id': 'outcome_person_',  # "Outcome.Person.."
        'table_email': 'out_email',
        '_table_name': ['outcome_person_name'],
        '_preprocess': lambda df: match_data.group_concat(df, ['outcome_person_', 'out_email', 'outcome_person_name'])
    },
    'volgistics': {
        '_label': 'volgistics',
        'table_id': 'Number'.lower(),
        'table_email': 'Email'.lower(),
        '_table_name': ['first_name_last_name']
    }
}  # TODO: consider other important fields, such as phone number


def start_flow():
    if os.listdir(CURRENT_SOURCE_FILES_PATH):
        pandas_tables = dict()
        for uploaded_file in os.listdir(CURRENT_SOURCE_FILES_PATH):
            file_path = os.path.join(CURRENT_SOURCE_FILES_PATH, uploaded_file)
            file_name_striped = file_path.split('/')[-1].split('-')[0]
            current_app.logger.info('running load_paws_data on: ' + uploaded_file)
            load_paws_data.load_to_postgres(file_path, file_name_striped, True)
            pandas_tables[file_name_striped] = match_data.read_from_postgres(file_name_striped)
            if '_preprocess' in MAPPING_FIELDS[file_name_striped]:
                pandas_tables[file_name_striped] = MAPPING_FIELDS[file_name_striped]['_preprocess'](pandas_tables[file_name_striped])
            pandas_tables[file_name_striped] = match_data.cleanup_and_log_table(pandas_tables[file_name_striped],
                MAPPING_FIELDS[file_name_striped],
                                                                                'excluded_' + file_name_striped + '.csv')

        with engine.connect() as connection:
            create_master_df.main(connection)


        # Match available data sources against salesforce
        matched_df = pd.DataFrame({'salesforce_id': []})  # init an empty dataframe for joining data from other sources
        for source in pandas_tables.keys():
            if source == 'salesforcecontacts':
                continue
            source_matches = match_data.match_cleaned_table(pandas_tables['salesforcecontacts'], pandas_tables[source], source, f'unmatched_{source}.csv')
            matched_df = matched_df.merge(source_matches, how='outer')

        ### New data flow, which will replace all of the matching logic above
        # Step 2: Compare data sources and dump in postgres (#78) -> rows to compare
        # e.g. { "new_rows": { "petpoint": [ { "id": 123, "all other petpoint rows": "etc" }, { "id": 122, "all other petpoint rows": "more fields here" } ], "volgistics": [ { "id": 1234, "all other volgistics rows": "all_of_them" } ], "all other sources like salesforce": [ { "all fields": "etc" } ] }, "updated_rows": { "old_id": "new_id", "old_id2": "new_id2", "old_id_n": "new_id_n" } }
        # AS THE INPUT TO THE NEW STEP: (TODO: refactor out of the flow script into match_data and a new function)
        # Step 3: Run the matching logic on the new records in priority order as established by
        # https://github.com/CodeForPhilly/paws-data-pipeline/blob/master/documentation/matching_rules.md
        # First, running transforms on this data for comparison sake....or actually just do it via LOWER() in SQL??
        match_criteria = ['email', 'name']
        table_priority = ['salesforcecontacts', 'volgistics', 'petpoint', 'ClinicHQ']
        
        def coalesce_fields_by_id(master_table, other_tables, master_ids, fields):
            # Add fields to master_table from other_tables, in priority order of how they're listed.
            # Similar in intent to running a SQL COALESCE based on the join to each field.
            df_with_updated_fields = master_table.copy()
            df_with_updated_fields[fields] = np.nan
            for table, table_id in zip(other_tables, table_ids):
                # may need to adjust the loop based on the master ID, renaming the fields, depending on how the PK is stored in the volgistics table, etc.
                fields_from_table = master_table.merge(table, how='left', validate='1:1')
                for field_to_update in fields:
                    df_with_updated_fields[field_to_update] = df_with_updated_fields[field_to_update].combine_first(fields_from_table[field_to_update])
            return df_with_updated_fields
        
        # Append fields from the source tables (Salesforce, volgistics, petpoint, etc.) in priority order
        master_df = coalesce_fields_by_id(
            _get_master_df(),
            [_get_most_recent_table_records_from_postgres(x) for x in table_priority],  # pseudo code
            [x+'id' for x in table_priority],
            match_criteria
        )
        # Then standardize the columns to match to avoid common/irrelevant sources of mismatching (lowercase, etc)
        def normalize_table_for_comparison(df):
            for column in match_criteria:
                df[column] = df[column].str.strip().str.lower()
            return df
        master_df = normalize_table_for_comparison(master_df)

        updated_master_rows = pd.DataFrame()
        new_master_rows = pd.DataFrame()
        for table in table_priority:
            #matches, left_only, right_only = attempt_to_join(master_df, pd.DataFrame(input_data['new_rows'][table]), match_criteria)
            def join_to_master(master_df, table_to_join):
                # attempts to join based on all columns
                left_right_indicator='_merge'
                join_results = master_df.merge(table_to_join, indicator=left_right_indicator)
                return (
                    join_results[join_results[left_right_indicator]=='left_only'].drop(columns=left_right_indicator),
                    join_results[join_results[left_right_indicator]=='right_only'].drop(columns=left_right_indicator),
                    join_results[join_results[left_right_indicator]=='both'].drop(columns=left_right_indicator)
                )
            updated_data_from_postgres = normalize_table_for_comparison(pd.DataFrame(input_data['new_rows'][table]))
            matches, left_only, right_only = join_on_all_columns(master_df, updated_data_from_postgres)
            updated_master_rows = updated_master_rows.append(matches)
            new_master_rows = new_master_rows.append(right_only)
            master_df = matches.append(left_only).append(right_only)
        # TODO: still need to reconcile the new and updated rows, especially based on duplicates...is it actually a new row?  Are we keeping the most recent update??
        # Alternatively, could just calculate the changes at the end
        #
        # Then pass updated_master_rows and new_master_rows to the next step in the data flow.
        ### end of new data flow ###

        matched_df.to_csv(os.path.join(LOGS_PATH, 'matches.csv'), index=False)

        # db_engine.dispose()  # we could close the db engine here once we're done with everything, but then it will be completely closed
        # See https://docs.sqlalchemy.org/en/13/core/connections.html#engine-disposal for design considerations.
