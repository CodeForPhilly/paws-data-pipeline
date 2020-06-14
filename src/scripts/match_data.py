# -*- coding: utf-8 -*-
import pandas as pd
import os

from fuzzywuzzy import fuzz
#from config import REPORT_PATH, engine
REPORT_PATH='fake'
engine='fake'  # TODO: removing these and restoring the module import
import datetime

TRANSFORM_EMAIL_NAME = 'lower_email'


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


class MismatchLogger:
    def __init__(self, reason_column='error_reason'):
        self.errors = pd.DataFrame()
        self.reason_column = reason_column
        
    def log_rows(self, error_df, reason_code='Reason not specified'):
        error_with_reason = error_df.copy()
        error_with_reason[self.reason_column] = reason_code
        self.errors = self.errors.append(error_with_reason)
    
    def write_log(self, file_basename, dir=REPORT_PATH):
        # Currently writing to a csv, but we could also consider a DB table
        # convention for logging, e.g. log_mismatch_salesforce_and_volgistics
        self.errors.to_csv(os.path.join(dir, file_basename), index=False)


def read_from_postgres(table_name):
    # Extracting pandas tables out from load_paws_data.load_to_sqlite
    #df = pd.read_sql_query("SELECT * FROM ?;", connection, params=(table_name))
    # Most SQL engines can only parameterize on literal values, not table names, so
    # let's format the SQL query another way for this internal API.
    # https://stackoverflow.com/questions/1274432/sqlite-parameters-not-allowing-tablename-as-parameter
    with engine.connect() as connection:
        df = pd.read_sql_query("SELECT * FROM {};".format(table_name), connection)

    return df


def remove_duplicates(df, field):
    duplicate_counts = df[field].value_counts()
    duplicate_ids = duplicate_counts[duplicate_counts.values > 1].index
    unique_rows = df[~df[field].isin(duplicate_ids)]
    duplicate_rows = df[df[field].isin(duplicate_ids)]
    return (unique_rows, duplicate_rows)

def group_concat(df, fields):
    # operates like the group_concat operator in SQL
    return df.groupby(fields).agg(list).reset_index()

def remove_null_rows(df, field):
    nonnull_rows = df[~df[field].isnull()]
    null_rows = df[df[field].isnull()]
    return (nonnull_rows, null_rows)

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


def test_start():
    # From GitHub: { "new_rows": { "petpoint": [ { "id": 123, "all other petpoint rows": "etc" }, { "id": 122, "all other petpoint rows": "more fields here" } ], "volgistics": [ { "id": 1234, "all other volgistics rows": "all_of_them" } ], "all other sources like salesforce": [ { "all fields": "etc" } ] }, "updated_rows": { "old_id": "new_id", "old_id2": "new_id2", "old_id_n": "new_id_n" } }
    
    # This is some of the example data for reference.  It should be deleted before merging back to master
    example_input_data = {'new_rows': {'salesforcecontacts': [('Loren Kiyota Household', '00339000029jzJn', 'Loren', 'Kiyota', None, '704 Wynnemoor Way', 'ORINDA', 'Co', '7701', 'US', None, None, None, 'pzv@b.scf', 'PAWS Development', '0013900001aGWYI', None, datetime.datetime(2020, 6, 9, 23, 2, 40, 67330), None), ('Lisa Trujillo Household', '00339000029k20k', 'Lisa', 'Trujillo', None, ' Moore Rd', None, None, None, None, None, None, None, None, 'PAWS Development', '0013900001aGXOd', None, datetime.datetime(2020, 6, 9, 23, 2, 40, 67330), None), ('Jade Thomas Bistro', '0033900002A03Vy', 'Jade', 'Thomas', None, '220 Annin St', 'MALVERN', 'Pennsylvania', '20009', 'US', '1276261767', None, '714 - 711-1110', 'mvkbtwogp@rgvqkued.egp', 'Lauren Hanak', '0013900001aGXZM', None, datetime.datetime(2020, 6, 9, 23, 2, 40, 67330), None), ('Jade Thomas Bistro', '00339000029k2Y3', 'Hannah', 'Rascon', None, '150 Chestnut St', 'Scotch Plain', 'IN', '18640-3525', 'US', '544 - 555-4550', None, '141 - 343-1454', 'xebqfclvop@qfrhgzkuo.xzi', 'Lauren Hanak', '0013900001aGXZM', None, datetime.datetime(2020, 6, 9, 23, 2, 40, 67330), None), ('Robert Flores Pub', '00339000029k2pA', 'Robert', 'Flores', None, '5818', 'Bristol', 'tokyo', '19123-2316', 'US', '235-235-5555', None, None, 'rapwxnko@ltkp.ect', 'PAWS Development', '0013900001aGXgw', None, datetime.datetime(2020, 6, 9, 23, 2, 40, 67330), None), ('Kale Wong Bistro', '00339000029k6Wq', 'Kale', 'Wong', None, '6555', 'North Hartland', 'Baden W?rttemberg', '60612', 'US', '3355333533', None, None, 'hemqwzu@tgcdy.hdy', 'PAWS Development', '0013900001aGYZh', None, datetime.datetime(2020, 6, 9, 23, 2, 40, 67330), None), ('Sean Tafoya Household', '00339000029kAQ7', 'Sean', 'Tafoya', None, '27 Edgewater Drive', 'Home', 'ID', '60643', 'US', '1421154224', None, None, 'ajetbxf@nszbimqcdu.mji', 'PAWS Development', '0013900001aGdOo', None, datetime.datetime(2020, 6, 9, 23, 2, 40, 67330), None), ('Fiona Price Pub', '0033p00002UO8aC', 'Fiona', 'Price', None, '55 Monument Rd', 'Barnwell', 'BaW?', '19142-2701', 'US', '1024144111', None, None, 'xogqmfwesz@lkhiq.puv', 'PAWS Development', '0013p00001pVtVA', None, datetime.datetime(2020, 6, 9, 23, 2, 40, 67330), None), ('Lars Duran Household', '0033p00002UO8ab', 'Lars', 'Duran', None, '2026 Luff Lane', 'Cave Creek', 'VA', '19152-2701', 'US', '227-207-3223', None, None, 'vzqgekdrc@tfh.wyi', 'PAWS Development', '0013p00001pVtVK', None, datetime.datetime(2020, 6, 9, 23, 2, 40, 67330), None), ('Edward Musso Household', '0033p00002UO8al', 'Edward', 'Musso', None, '2222 Rancocas Road', 'Bethesda', 'CT', '6026', 'US', '1222104212', None, None, 'gwua@tkx.jch', 'PAWS Development', '0013p00001pVtVU', None, datetime.datetime(2020, 6, 9, 23, 2, 40, 67330), None), ('Angelica el-Ashraf Bistro', '0033p00002UO8dB', 'Angelica', 'el-Ashraf', None, '1417 Estate', 'Fontana', 'Pennsvania', '19119-3111', 'US', None, None, None, 'pxm@bnygeuzhvo.ewu', 'PAWS Development', '0013p00001pVtVy', None, datetime.datetime(2020, 6, 9, 23, 2, 40, 67330), None), ('Cassondra el-Kamal Household', '0033p00002UO8ed', 'Cassondra', 'el-Kamal', None, '2210 S. 14st Street', 'West Portsmouth', 'NH', '19125-3329', 'US', None, None, None, 'ske@ciqgr.ndf', 'PAWS Development', '0013p00001pVtWX', None, datetime.datetime(2020, 6, 9, 23, 2, 40, 67330), None), ('Justin Campbell Bistro', '0033p00002UO8oS', 'Justin', 'Campbell', None, '4074 S. 41rd St.', 'Ocean', 'Texas', '19474-0204', None, None, None, None, 'faxh@lcume.enj', 'Jared Hupp', '0013p00001pVtaP', None, datetime.datetime(2020, 6, 9, 23, 2, 40, 67330), None), ('Aslam Wilson Household', '0033p00002UO8q2', 'Aslam', 'Wilson', None, '222 n Columbus blvd', 'New Haven', 'BC', '17009', 'US', '4146143364', None, None, 'tpik@wotkn.qwi', 'PAWS Development', '0013p00001pVtaj', None, datetime.datetime(2020, 6, 9, 23, 2, 40, 67330), None), ('Dashawn Patterson Household', '0033p00002UO8tB', 'Dashawn', 'Patterson', None, '311', 'High Bridge', 'WA', '19064-3130', None, None, None, None, 'nobcuvj@blyh.zva', 'Jared Hupp', '0013p00001pVtbS', None, datetime.datetime(2020, 6, 9, 23, 2, 40, 67330), None), ('Lorem Ipsum Household', '0013900001aO4Sj', 'Lorem', 'Ipsum', None, '33 Drury Lane', 'Nowhere', 'Pa', '7701', 'US', '222-444-5555', None, None, 'lorem@gmail.com', 'PAWS Development', '0013900001aGWYI', None, datetime.datetime(2020, 6, 9, 23, 2, 40, 67330), None), ('Jim Bean Household', '0013900001aGYZh', 'Jim', 'Bean', None, None, 'Philadelphia', 'PA', None, 'US', '3355333533', None, None, 'jimb3@gmail.com', 'PAWS Development', '0013900001aGWYJ', None, datetime.datetime(2020, 6, 9, 23, 2, 40, 67330), None), ('Jane Doe Household', '0013900001aGXOd', 'Jane', 'Doe', None, '33 Drury Lane', 'Nowhere', 'Pa', '7701', 'US', '333-555-6666', None, None, 'jane@gmail.com', 'PAWS Development', '0013900001aGWYK', None, datetime.datetime(2020, 6, 9, 23, 2, 40, 67330), None)], 'volgistics': [('Ipsum, Lorem', 'Lorem Ipsum', 'Mr. Lorem Ipsum', 'Ipsum', 'Lorem', None, 'Mr.', None, 'Active', None, None, 'Individual', None, None, None, 8362124, '3203 Castor Ave SCHWENKSVILLE, 19141', '3203 Castor Ave', None, None, 'SCHWENKSVILLE', None, '19141', None, None, None, None, '222-444-5555 (Home) (Work) (141) 271-3020 (Cell)', '222-444-5555', None, None, None, '(141) 271-3020', 'Yes', None, None, None, None, None, None, None, 'lorem@gmail.com', None, 2.0, 0, 0, 0, 0, 0, 0, 0, 2.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '6/10/2018', '6/10/2018', None, None, '14-Aug', '14-Aug', 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'Yes', 'Yes', 'Yes', None, None, None, 0, None, datetime.datetime(2020, 6, 9, 23, 2, 40, 205263), None), ('Robinson, Prerit', 'Prerit Robinson', 'Mrs. Prerit Robinson', 'Robinson', 'Prerit', None, 'Mrs.', None, 'Active', None, None, 'Individual', None, None, None, 6011436, '281 Marvin Road GLENSIDE, NY 19020-6449', '281 Marvin Road', None, None, 'GLENSIDE', 'NY', '19020-6449', None, None, None, None, '(955) 451-5055 (Home) (Work) (Cell)', '(955) 451-5055', 'Yes', None, None, None, None, None, None, None, None, None, None, None, 'k@kemhgj.xhr', None, 0.0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '3/14/2018', '3/14/2018', None, None, '27-Apr', '27-Apr', 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'Yes', None, 'Yes', None, None, None, 0, None, datetime.datetime(2020, 6, 9, 23, 2, 40, 205263), None), ('el-Mousa, Shayana', 'Shayana el-Mousa', ' Shayana el-Mousa', 'el-Mousa', 'Shayana', None, None, "Pronounced 'Ni-tasha'", 'Active', None, None, 'Individual', None, None, None, 8249492, '999 Hermesprota Drive Rockledge, NJ 17109', '999 Hermesprota Drive', None, None, 'Rockledge', 'NJ', '17109', None, None, None, None, '(864) 474-4478 (Home) (Work) (Cell)', '(864) 474-4478', 'Yes', None, None, None, None, None, None, None, None, None, None, None, 'ezsrdnyp@kyc.osk', None, 43.0, 0, 0, 0, 1, 0, 1, 0, 29.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '10/2/2017', '10/2/2017', None, None, '12-Nov', '12-Nov', 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'Yes', None, 'Yes', None, None, None, 0, None, datetime.datetime(2020, 6, 9, 23, 2, 40, 205263), None), ('Garduno, April', 'April Garduno', ' April Garduno', 'Garduno', 'April', None, None, None, 'Active', None, None, 'Individual', None, None, None, 482957, '4433 Sansom St. , ', '4433 Sansom St.', None, None, None, None, None, None, None, None, None, ' (Home) (Work) (Cell)', None, None, None, None, None, None, None, None, None, None, None, None, None, 'ah@one.xsa', None, 0.0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '4/2/2017', '4/2/2017', None, None, None, None, 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'Yes', None, 'Yes', None, None, None, 0, None, datetime.datetime(2020, 6, 9, 23, 2, 40, 205263), None), ('Campa, Taahir', 'Taahir Campa', 'Ms. Taahir Campa', 'Campa', 'Taahir', None, 'Ms.', None, 'Active', None, None, 'Individual', None, None, None, 6850005, '3103 Sussex Lane Willow Grove, UT 19121', '3103 Sussex Lane', None, None, 'Willow Grove', 'UT', '19121', None, None, None, None, '(303) 430-1004 (Home) (Work) (Cell)', '(303) 430-1004', 'Yes', None, None, None, None, None, None, None, None, None, None, None, 'zfcl@lidczsrqb.seg', None, 2.0, 0, 0, 0, 0, 0, 0, 0, 2.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '2/7/2018', '2/7/2018', None, None, '6-Jun', '6-Jun', 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'Yes', None, 'Yes', None, None, None, 0, None, datetime.datetime(2020, 6, 9, 23, 2, 40, 205263), None), ('Meza, Courtni', 'Courtni Meza', ' Courtni Meza', 'Meza', 'Courtni', None, None, None, 'Active', None, None, 'Individual', None, None, None, 3351445, '2200 S. 62th Street Mullica Hill, DE 19131', '2200 S. 62th Street', None, 'Phildelphia', 'Mullica Hill', 'DE', '19131', None, None, None, None, '(966) 363-6666 (Home) (Work) (888) 822-5828 (Cell)', '(966) 363-6666', 'Yes', None, None, '(888) 822-5828', 'Yes', None, None, None, None, None, None, None, 'sanl@hszcnmi.pgq', None, 14.96666667, 0, 0, 0, 0, 0, 0, 0, 14.96666667, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '6/7/2018', '6/7/2018', None, None, '7-Nov', '7-Nov', 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'Yes', 'Yes', 'Yes', None, None, None, 0, None, datetime.datetime(2020, 6, 9, 23, 2, 40, 205263), None), ('Johnson, Billy', 'Billy Johnson', ' Billy Johnson', 'Johnson', 'Billy', None, None, 'Antonio', 'Active', None, None, 'Individual', None, None, None, 670709, '2101 Frankford Ave Willow Grove, UT 19119', '2101 Frankford Ave', None, None, 'Willow Grove', 'UT', '19119', None, None, None, None, '(212) 622-2122 (Home) (Work) (Cell)', '(212) 622-2122', 'Yes', None, None, None, None, None, None, None, None, None, None, None, 'qlmtni@uwknrxbos.aex', None, 2.0, 0, 0, 0, 0, 0, 0, 0, 2.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '1/2/2018', '1/2/2018', None, None, '16-Mar', '16-Mar', 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'Yes', None, 'Yes', None, None, None, 0, None, datetime.datetime(2020, 6, 9, 23, 2, 40, 205263), None), ('el-Naqvi, Tony', 'Tony el-Naqvi', ' Tony el-Naqvi', 'el-Naqvi', 'Tony', None, None, None, 'Active', None, None, 'Individual', None, None, None, 6747843, '11 W. Queen Lane merion, DE 19010', '11 W. Queen Lane', None, None, 'merion', 'DE', '19010', None, None, None, None, '(911) 621-6866 (Home) (Work) (362) 113-6216 (Cell)', '(911) 621-6866', 'Yes', None, None, '(362) 113-6216', 'Yes', None, None, None, None, None, None, None, 'vwjnktaoxu@kixhren.ots', None, 0.0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '4/6/2018', '4/10/2018', None, None, '24-Mar', '24-Mar', 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'Yes', 'Yes', 'Yes', None, None, None, 0, None, datetime.datetime(2020, 6, 9, 23, 2, 40, 205263), None), ('Berg, Abigale', 'Abigale Berg', ' Abigale Berg', 'Berg', 'Abigale', None, None, None, 'Active', None, None, 'Individual', None, None, None, 684447, '222 Mitchell Street Lansdale, UT 19002', '222 Mitchell Street', None, None, 'Lansdale', 'UT', '19002', None, None, None, None, '(929) 199-1991 (Home) (124) 522-5225 (Work) (Cell)', '(929) 199-1991', None, '(124) 522-5225', None, None, None, None, None, None, None, None, None, None, 'pd@delmtb.zjq', None, 80.25, 0, 0, 0, 0, 0, 0, 0, 13.25, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '11/24/2014', '11/24/2014', None, None, None, None, 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'Yes', None, 'Yes', None, None, None, 0, None, datetime.datetime(2020, 6, 9, 23, 2, 40, 205263), None), ('el-Radi, Shania', 'Shania el-Radi', ' Shania el-Radi', 'el-Radi', 'Shania', None, None, None, 'Active', None, None, 'Individual', None, None, None, 555054, '22039 Chestnut Street, Lansdale, NY 19154', '22039 Chestnut Street,', None, None, 'Lansdale', 'NY', '19154', None, None, None, None, '(239) 292-4041 (Home) (Work) (141) 131-5051 (Cell)', '(239) 292-4041', 'Yes', None, None, '(141) 131-5051', None, None, None, None, None, None, None, None, 'tuyrlmxd@jokr.frn', None, 0.0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '10/24/2017', '10/25/2017', None, None, '4-Oct', '4-Oct', 0, None, None, None, None, None, None, '10/1/2017', None, None, None, None, None, None, None, None, None, None, None, 'Yes', None, 'Yes', None, None, None, 0, None, datetime.datetime(2020, 6, 9, 23, 2, 40, 205263), None), ('bean, jim', 'jim bean', 'jim bean', 'bean', 'jim', None, None, None, 'Active', None, None, 'Individual', None, None, None, 762713, '555 n. 24th St. Selinsgrove, 19132', '555 n. 24th St.', '3303', None, 'Selinsgrove', None, '19132', None, None, None, None, ' (Home) (Work) (Cell)', None, None, None, None, None, None, None, None, None, None, None, None, None, 'JIMB3@gmail.com', None, 0.0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '5/29/2018', '5/29/2018', None, None, None, None, 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'Yes', 'Yes', 'Yes', None, None, None, 0, None, datetime.datetime(2020, 6, 9, 23, 2, 40, 205263), None), ('Plascencia, Ilhaam', 'Ilhaam Plascencia', ' Ilhaam Plascencia', 'Plascencia', 'Ilhaam', None, None, None, 'Active', None, None, 'Individual', None, None, None, 257288, '2888 S Juniper Street , ', '2888 S Juniper Street', None, None, None, None, None, None, None, None, None, '(316) 331-0336 (Home) (Work) (Cell)', '(316) 331-0336', 'Yes', None, None, None, None, None, None, None, None, None, None, None, 'buakzpn@y.zue', None, 8.416666667, 0, 1, 0, 1, 0, 2, 0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '3/29/2017', '3/29/2017', None, None, None, None, 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'Yes', None, 'Yes', None, None, None, 0, None, datetime.datetime(2020, 6, 9, 23, 2, 40, 205263), None), ('el-Mousa, Mahmood', 'Mahmood el-Mousa', 'Ms. Mahmood el-Mousa', 'el-Mousa', 'Mahmood', None, 'Ms.', None, 'Active', None, None, 'Individual', None, None, None, 7023174, '6664 Pine St Doylestown, 19020', '6664 Pine St', 'Apt. 401', None, 'Doylestown', None, '19020', None, None, None, None, '(111) 110-1112 (Home) (Work) (Cell)', '(111) 110-1112', 'Yes', None, None, None, None, None, None, None, None, None, None, None, 'tp@xt.efv', None, 4.25, 0, 0, 0, 0, 0, 0, 0, 4.25, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '3/29/2018', '3/29/2018', None, None, '21-Jul', '21-Jul', 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'Yes', None, 'Yes', None, None, None, 0, None, datetime.datetime(2020, 6, 9, 23, 2, 40, 205263), None), ('al-Mattar, Alyssa', 'Alyssa al-Mattar', 'Ms. Alyssa al-Mattar', 'al-Mattar', 'Alyssa', None, 'Ms.', None, 'Active', None, None, 'Individual', None, None, None, 331952, '4201 Lansing Street Bala Cynwyd, WI 19083', '4201 Lansing Street', None, None, 'Bala Cynwyd', 'WI', '19083', None, None, None, None, ' (Home) (Work) (454) 504-4444 (Cell)', None, None, None, None, '(454) 504-4444', None, None, None, None, None, None, None, None, 'zwyf@l.rcd', None, 17.16666667, 0, 0, 0, 2, 0, 2, 0, 3.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '11/21/2016', '11/21/2016', None, None, '9-Jan', '9-Jan', 0, None, None, None, None, None, None, '11/13/2016', None, None, None, None, None, None, None, None, None, None, None, 'Yes', None, 'Yes', None, None, None, 0, None, datetime.datetime(2020, 6, 9, 23, 2, 40, 205263), None), ('Phillips, Shadawn', 'Shadawn Phillips', 'Ms. Shadawn Phillips', 'Phillips', 'Shadawn', None, 'Ms.', None, 'Active', None, None, 'Individual', None, None, None, 98785, '112 Old Penllyn Pike Philadelphia, Pa, CA 10003', '112 Old Penllyn Pike', None, None, 'Philadelphia, Pa', 'CA', '10003', None, None, None, None, '(105) 510-2111 (Home) (555) 555-5555 (Work) (Cell)', '(105) 510-2111', 'Yes', '(555) 555-5555', 'Yes', None, None, None, None, None, None, None, None, None, 'c@tmcgurb.vwo', None, 4.0, 0, 0, 0, 0, 0, 0, 0, 4.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '11/2/2017', '11/3/2017', None, None, '8-Jun', '8-Jun', 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'Yes', None, 'Yes', None, None, None, 0, None, datetime.datetime(2020, 6, 9, 23, 2, 40, 205263), None), ('el-Majeed, Carolina', 'Carolina el-Majeed', 'Ms. Carolina el-Majeed', 'el-Majeed', 'Carolina', None, 'Ms.', None, 'Active', None, None, 'Individual', None, None, None, 524505, '25 E. Salmon Street Havertown, PA 19104', '25 E. Salmon Street', 'Apt B2', None, 'Havertown', 'PA', '19104', None, None, None, None, '(434) 440-3444 (Home) (Work) (Cell)', '(434) 440-3444', 'Yes', None, None, None, None, None, None, None, None, None, None, None, 'znyqcguaod@qfsmertaz.gli', None, 0.0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '9/25/2017', '9/25/2017', None, None, None, None, 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'Yes', None, 'Yes', None, None, None, 0, None, datetime.datetime(2020, 6, 9, 23, 2, 40, 205263), None)], 'petpoint': [('A37324077', None, 'Wendy Willow Puffs', 'Cat', 'Cat', 'Domestic Shorthair', 'Mix', None, 'F', 'Yes', 'No', None, None, None, '6 months to 1 year', None, 'Healthy', 'Adriana Miller', '12/6/2017 9:21', 'Transfer In', 'Partner Transfer In', None, 19106.0, 'Rescue', 'Grays Ferry Avenue', None, 'Cumberland County SPCA', 'Shannon Abbott', '(146) 655-5400', '1244 N Delsea Drive ', None, None, 'P28349659', 'William Johnson', None, None, None, None, None, None, None, None, None, 'saemwtqnc@te.coy', None, None, 'New Arrival', None, None, '12/20/2017 0:00', '24PetWatch', '322222000000000', None, None, 'I', 'Released', 'Released', None, None, 246.0, 'Lucero, Adrian', '12/23/2017 18:07', '12/23/2017 18:06', '12/23/2017 18:06', 'Adoption', 'PAC', 'PAWS Offsite Adoptions', None, None, '67006037', 'Government ID', 'P29555713', 'Lorem Ipsum', '3313', '29th', 'Walk', None, None, None, 'PHILADELPHIA', 'PA', 8638.0, 'lorem@gmail.com', '(222) 444-5555', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, datetime.datetime(2020, 6, 9, 23, 2, 40, 523042), None), ('A37493839', None, 'Matilda', 'Dog', 'Dog', 'Pomeranian', 'Mix', None, 'F', 'Yes', 'No', None, None, None, '6 to 10 years', 'Healthy', 'Healthy', 'Vandell Eugene', '12/29/2017 16:49', 'Stray', 'Public Drop Off', 'Found near 3200 Comly Rd', 19146.0, None, 'Grant Avenue', 'Northeast Philadelphia', None, None, None, None, None, None, 'P11975244', 'Raymond Soe', 1373.0, 'Browning', 'Parkway', 'S ', None, None, 'PHILADELPHIA', 'PA', 19074.0, None, '(782) 870-8872', None, 'New Arrival', None, None, '1/2/2018 0:00', '24PetWatch', '646264000000000', None, None, 'I', 'Released', 'Released', None, 'Healthy', 3617.0, 'Burnett, Sadyan', '1/2/2018 17:46', '1/2/2018 17:45', '1/2/2018 17:45', 'Return to Owner/Guardian', 'Stray Reclaim', 'Grant Avenue', None, None, '24 083 078', 'Driver License', 'P29613725', 'Lorem Ipsum', '11137', 'Bustleton', 'Avenue', None, None, '324', 'PHILADELPHIA', 'PA', 19008.0, 'lorem@gmail.com', '(222) 444-5555', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, datetime.datetime(2020, 6, 9, 23, 2, 40, 523042), None), ('A37498706', None, 'Niles', 'Cat', 'Cat', 'Domestic Shorthair', 'Mix', None, 'M', 'No', 'No', None, None, None, '1 to 2 years', 'Healthy', 'Healthy', 'Rachel Jones', '12/30/2017 15:17', 'Stray', 'Public Drop Off', '19154', 19154.0, None, 'Grays Ferry Avenue', 'Southwest Philadelphia', None, None, None, None, None, None, 'P02401272', 'Jaasim al-Popal', 11011.0, 'Heflin', 'Road', None, None, None, 'PHILADELPHIA', 'PA', 8053.0, None, '(141) 111-1111', None, 'New Arrival', None, None, '12/30/2017 0:00', '24PetWatch', '372000000000000', None, None, 'I', 'Released', 'Released', None, 'Healthy', 3618.0, 'Hebert, Sharden', '1/2/2018 12:52', '1/2/2018 12:51', '1/2/2018 12:51', 'Return to Owner/Guardian', 'Stray Reclaim', 'Grant Avenue', None, None, None, None, 'P29598889', 'Jane Doe', '4410', 'Wayne', 'Drive', None, None, '2212', 'PHILADELPHIA', 'PA', 8638.0, 'jane@gmail.com', None, '(333) 555-6666', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, datetime.datetime(2020, 6, 9, 23, 2, 40, 523042), None), ('A37545883', None, 'Torty', 'Cat', 'Cat', 'Domestic Shorthair', 'Mix', None, 'F', 'Yes', 'No', None, None, None, '1 to 2 years', 'Healthy', 'Healthy', 'Jazmin Ortega', '1/6/2018 12:51', 'Stray', 'Public Drop Off', 'Found at 4000 block Higbee St', 19135.0, None, 'Grant Avenue', 'Northeast Philadelphia', None, None, None, None, '12 308 182', 'Driver License', 'P29641319', 'Shantavia Pittman Jr', 4050.0, 'Washburn', 'Pike', None, None, None, 'PHILADELPHIA', 'PA', 19138.0, None, '(227) 237-7003', None, 'New Arrival', None, None, '1/6/2018 0:00', '24PetWatch', '121000000000000', None, None, 'I', 'Released', 'Released', None, 'Healthy', 3620.0, 'Andrade, Samantha', '1/11/2018 16:23', '1/11/2018 16:22', '1/11/2018 16:22', 'Return to Owner/Guardian', 'Stray Reclaim', 'Grant Avenue', None, None, '62 666 226', 'Driver License', 'P29680049', 'Antonio Williams', '3333', 'McKean', 'Square', None, None, None, 'PHILADELPHIA', 'PA', 18940.0, None, '(444) 444-4444', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, datetime.datetime(2020, 6, 9, 23, 2, 40, 523042), None), ('A37547588', None, 'Kit', 'Cat', 'Cat', 'Domestic Shorthair', 'Mix', None, 'M', 'Yes', 'No', None, None, None, '6 to 10 years', 'Unhealthy/Untreatable', 'Sick', 'Nawfa el-Baig', '1/5/2018 15:29', 'Stray', 'Abandoned at Shelter', 'abandoned in hallway', 19106.0, None, 'Grant Avenue', 'Jurisdiction Unknown', None, None, None, None, None, None, 'P00000001', None, None, None, None, None, None, None, None, None, None, None, None, None, 'New Arrival', None, None, None, None, None, None, None, 'H', 'Released', 'Released', None, 'Unhealthy/Untreatable', 1584.0, None, '1/6/2018 16:06', '1/6/2018 15:36', None, 'Euthanasia', '35 Non Treatable Medical', 'Grant Avenue', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, datetime.datetime(2020, 6, 9, 23, 2, 40, 523042), None), ('A37664421', None, 'Sasa fka Jabber Jenny', 'Cat', 'Cat', 'Domestic Shorthair', 'Mix', None, 'F', 'Yes', 'No', None, None, None, '2 to 4 years', None, 'Healthy', 'Naadir el-Bacchus', '1/22/2018 14:39', 'Stray', 'Public Drop Off', '27XX Cantrell Terrace', 19145.0, None, 'Grays Ferry Avenue', '19145— South Philadelphia W', None, None, None, None, '81621868', 'Driver License', 'P16824547', 'Arshad el-Atallah', 4226.0, 'Hastings', 'Terrace', None, None, None, 'PHILADELPHIA', 'PA', 19111.0, None, '(377) 700-7732', None, 'New Arrival', None, None, '1/25/2018 0:00', '24PetWatch', '323435000000000', None, None, 'I', 'Released', 'Released', None, None, 1913.0, 'Som, Sokdaney', '2/23/2018 18:24', '2/23/2018 18:23', '2/23/2018 18:23', 'Adoption', 'Foster Home', 'PAWS Foster Program', None, None, '88888888', 'Driver License', 'P29552904', 'Brianna Palmier', '9550', 'Mt. Vernon', 'Alley', 'S ', None, None, 'PHILADELPHIA', 'PA', 19047.0, 'gmfnpx@njvmfb.vto', '(255) 265-1255', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, datetime.datetime(2020, 6, 9, 23, 2, 40, 523042), None), ('A37926328', None, 'Pauly', 'Cat', 'Cat', 'Domestic Shorthair', 'Mix', None, 'M', 'No', 'No', None, None, None, '6 to 10 years', None, 'Sick', 'Ummu Kulthoom al-Reza', '2/25/2018 14:06', 'Stray', 'Abandoned at Shelter', 'uber driver says cat was abandoned in vehicle', 19106.0, None, 'Grays Ferry Avenue', 'Jurisdiction Unknown', None, None, None, None, None, None, 'P00000001', None, None, None, None, None, None, None, None, None, None, None, None, None, 'New Arrival', None, None, '2/25/2018 0:00', '24PetWatch', '0A16661111', None, None, 'I', 'Released', 'Released', None, None, 3627.0, 'Thompson, Jaylyn', '2/26/2018 10:45', '2/26/2018 10:43', '2/26/2018 10:43', 'Return to Owner/Guardian', 'Stray Reclaim', 'Grays Ferry Avenue', None, None, None, None, 'P29991097', 'Marcus Mack', '21', '5th', 'Drive', None, None, None, 'PHILADELPHIA', 'PA', 18902.0, None, '(214) 101-5514', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, datetime.datetime(2020, 6, 9, 23, 2, 40, 523042), None), ('A37931542', None, 'Purrfesional Furrtographer Swingster Furman', 'Cat', 'Cat', 'Domestic Shorthair', 'Mix', None, 'F', 'Yes', 'No', None, None, None, '6 months to 1 year', None, 'Healthy', 'Caleb Stock', '2/26/2018 13:09', 'Stray', 'Public Drop Off', 'unknown', 19405.0, None, 'Grays Ferry Avenue', 'PA Outside City Limits', None, None, None, None, None, None, 'P22944371', 'Shareefa el-Dallal', 110.0, 'Perrin', 'Drive', 'W ', None, None, 'BRIDGEPORT', 'PA', 19128.0, None, '(224) 200-4244', None, 'New Arrival', None, None, '2/26/2018 0:00', '24PetWatch', '634244000000000', None, None, 'I', 'Released', 'Released', None, None, 2699.0, 'Mcknight, Jasmine', '2/28/2018 17:08', '2/28/2018 17:07', '2/28/2018 17:07', 'Adoption', 'PAC', 'PAWS Offsite Adoptions', None, None, '11342333', 'Driver License', 'P30011046', 'Rayanne Williams', '6630A', 'Woodhaven', 'Lane', None, None, 'B4', 'PHILADELPHIA', 'PA', 19074.0, 'jabsg@ixbagpd.ucs', '(744) 334-0347', '(143) 101-1333', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, datetime.datetime(2020, 6, 9, 23, 2, 40, 523042), None), ('A37988069', None, 'Maple', 'Dog', 'Dog', 'Terrier', 'Mix', None, 'F', 'No', 'No', None, None, None, '6 months to 1 year', None, 'Sick', 'Juan Bautista', '3/5/2018 15:19', 'Owner/Guardian Surrender', 'ACCT Diversion', None, 19133.0, 'Health of Animal', 'Grays Ferry Avenue', None, None, None, None, None, '23214124', 'Driver License', 'P30043595', 'Harley Mestas', 2555.0, 'Saint Elmo', 'Circle', 'N ', None, None, 'PHILADELPHIA', 'PA', 10457.0, 'cpz@doaceiqpj.med', '(445) 600-4546', None, 'New Arrival', None, None, None, None, None, None, None, 'H', 'Released', 'Released', None, None, 3.0, None, '3/6/2018 10:38', '3/6/2018 10:37', None, 'Died', 'General', 'Grays Ferry Avenue', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, datetime.datetime(2020, 6, 9, 23, 2, 40, 523042), None), ('A38026536', None, 'Lily of the Valley', 'Cat', 'Cat', 'Domestic Shorthair', 'Mix', None, 'F', 'Yes', 'No', None, None, None, '6 months to 1 year', None, 'Healthy', 'Luisa Hamilton', '3/9/2018 15:29', 'Stray', 'Public Drop Off', 'abandoned on side of road', 19405.0, None, 'Grays Ferry Avenue', 'PA Outside City Limits', None, None, None, None, None, None, 'P22944371', 'Matthew Castillo', 440.0, '2ND', 'Street', 'W ', None, None, 'BRIDGEPORT', 'PA', 8057.0, None, '(426) 400-6433', None, 'New Arrival', None, None, '3/9/2018 0:00', '24PetWatch', '424442000000000', None, None, 'I', 'Released', 'Released', None, None, 2688.0, 'al-Azizi, Almaasa', '3/17/2018 13:09', '3/17/2018 ', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, datetime.datetime(2020, 6, 9, 23, 2, 40, 523042), None), ('3/17/2018 13:08', 'Adoption', 'PAC', 'PAWS Offsite Adoptions', None, None, '46446042', 'Driver License', 'P30125607', 'David Prum', '8222', 'Venus', 'Crossing', None, None, '223', 'PHILADELPHIA', 'PA', '19342', 'bdh@ie.hzm', None, '(630) 266-0666', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, datetime.datetime(2020, 6, 9, 23, 2, 40, 523042), None)]}, 'updated_rows': {}}

    print(start(example_input_data))

# TODO: also remove
if __name__ == '__main__':
    test_start()
# TODO: clean up the old code below and in the header

def cleanup_and_log_table(df, important_fields, log_name='mismatches.csv'):
    cleaned_df = df.copy()
    for renamed, orig in important_fields.items():
        if renamed.startswith('_'):
            continue
        cleaned_df[renamed] = cleaned_df[orig]
    
    # Reconstructing names, allowing for it to be split across multiple fields
    cleaned_df['table_name'] = cleaned_df[important_fields['_table_name'][0]]
    for i in range(1, len(important_fields['_table_name'])):
        cleaned_df['table_name'] = cleaned_df['table_name'] + ' ' + cleaned_df[important_fields['_table_name'][i]]
    
    # Applying a lowercase filter to email for matching purposes, since the case is usually
    # inconsistent, and logging potential issues for matching (as well as duplicate/null ID's,
    # which would also be unexpected in a clean data source)
    cleaned_df[TRANSFORM_EMAIL_NAME] = cleaned_df['table_email'].str.lower()
    mismatches = MismatchLogger()
    for cleanup_field in [TRANSFORM_EMAIL_NAME, 'table_id']:
        cleaned_df, null_df = remove_null_rows(cleaned_df, cleanup_field)
        mismatches.log_rows(null_df, 'Null {}'.format(cleanup_field))
        cleaned_df, duplicate_df = remove_duplicates(cleaned_df, cleanup_field)
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
    fuzzy_output_field = table_name + '_fuzzy_name_score'

    # Match by email
    matched, unmatched_salesforce, unmatched_table = match_by_field(
            salesforce_df[['table_id', TRANSFORM_EMAIL_NAME]],
            table_df[['table_id', TRANSFORM_EMAIL_NAME]],
            output_ids=[salesforce_id_field, table_id_field],
            match_field=TRANSFORM_EMAIL_NAME,
            id_field='table_id'
    )
    # Apply fuzzy matching on names
    matched = (
        matched
        .merge(salesforce_df[['table_id', 'table_name']].rename(columns={'table_name': salesforce_name_field, 'table_id': salesforce_id_field}))
        .merge(table_df[['table_id', 'table_name']].rename(columns={'table_name': table_name_field, 'table_id': table_id_field}))
    )
    unmatched_table = unmatched_table.merge(table_df[['table_id', 'table_name']].rename(columns={'table_name': table_name_field, 'table_id': table_id_field}))
    matched[fuzzy_output_field] = df_fuzzy_score(matched, table_name_field, salesforce_name_field)
    unmatched_by_name = matched[matched[fuzzy_output_field] != 100].copy()
    matched = matched[matched[fuzzy_output_field] == 100]

    # TODO: ANY OTHER MATCH DOCUMENTATION TO ADD OR MODIFY FROM MEG, CHRIS, AND KARLA?

    # Log mismatches from the new table
    mismatches = MismatchLogger()
    mismatches.log_rows(unmatched_table, 'Email not found in Salesforce')
    mismatches.log_rows(unmatched_by_name, 'Name did not match Salesforce')
    mismatches.write_log(log_name)

    return matched

