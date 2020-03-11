import sqlite3
import pandas as pd
import numpy as np
import re
from functools import reduce
import json
#from postal.expand import expand_address

# import data and clean columns
def import_csv_and_clean_cols(csv, drop_first_col=False):
    
    df = pd.read_csv(csv, encoding='cp1252', dtype=str)
    
    # drop the first column - so far all csvs have had a first column that's an index and doesn't have a name
    if drop_first_col:
        df = df.drop(df.columns[0], axis=1)
    
    # strip whitespace and periods from headers, convert to lowercase
    df.columns = df.columns.str.lower().str.strip()
    df.columns = df.columns.map(lambda x: re.sub(r'\s+', '_', x))
    df.columns = df.columns.map(lambda x: re.sub(r'\.+', '_', x))
    
    return df

def clean_entries(entry):
    """
    1 Change 'None' or 'NaN' value to an empty string
    2 Cast value as string
    3 Lowercase value
    3 Strip leading and trailing white space
    4 Replace internal multiple consecutive white spaces with a single white space
    """
    
    # convert None and NaN to an empty string. This allows simple string concatenation
    if pd.isnull(entry):
        entry = ''
    
    # convert to string, lowercase, and strip leading and trailing whitespace
    entry = str(entry).lower().strip()
    
    # cut down (internal) consecutive whitespaces to one white space
    entry = re.sub(r'\s+', ' ', entry)
    
    return entry

def strip_symbols(char_string, kept_chars = '- 1234567890abcdefghijklmnopqrstuvwxyz'):
    
    '''
    strip all characters from the passed string that are not specified in kept_chars.
    the base case keeps only letters, numbers, spaces, and dashes.
    while this is fine for most string entries, the default selection is not appropriate for 
    all entries. For instance, email addresses can contain various characters and are best left intact.
    '''

    return ''.join([c for c in char_string if c in kept_chars])

def combine_address_columns(address_columns):
    return reduce(lambda col_1, col_2: 
        col_1.apply(clean_entries).apply(strip_symbols) + ' ' + 
        col_2.apply(clean_entries).apply(strip_symbols), address_columns).apply(clean_entries)

# load dataframe into database table, drop and replace the table if it exists
def load_to_sqlite(df, table_name, connection):
    df.to_sql(table_name, connection, if_exists='replace', index=False)

if __name__ == "__main__":
    # connect to or create database
    conn = sqlite3.connect("../../sample_data/paws.db")

    # I acknowledge that dumping the list of expanded addresses to json is not the right thing to do with an RDBMS, but here we are. To read back to a list run json.loads()
    
    # petpoint
    petpoint_df = import_csv_and_clean_cols('../../sample_data/CfP_PDP_petpoint_deidentified.csv', drop_first_col=True)

    petpoint_df['match_name'] = petpoint_df['outcome_person_name'].apply(clean_entries).apply(strip_symbols)
    petpoint_df['match_email'] = petpoint_df['out_email'].apply(clean_entries)
    petpoint_df['match_cell'] = petpoint_df['out_cell_phone'].apply(clean_entries).apply(strip_symbols)
    petpoint_df['match_phone'] = petpoint_df['out_home_phone'].apply(clean_entries).apply(strip_symbols)

    addr_components = [petpoint_df['out_street_name'], petpoint_df['out_street_type'], petpoint_df['out_street_direction'], petpoint_df['out_street_direction2'], petpoint_df['out_unit_number'], petpoint_df['out_city'], petpoint_df['out_province'], petpoint_df['out_postal_code'].fillna('').apply(str).str[:5]]
    petpoint_df['match_address_list'] = combine_address_columns(addr_components)
    #petpoint_df['match_address_list'] = petpoint_df['match_address_list'].apply(expand_address, languages=['en']).apply(json.dumps)

    load_to_sqlite(petpoint_df, 'petpoint', conn)

    # volgistics
    volgistics_df = import_csv_and_clean_cols('../../sample_data/CfP_PDP_volgistics_deidentified.csv', drop_first_col=True)

    volgistics_df['match_name'] = volgistics_df['last_name_first_name'].apply(clean_entries).apply(strip_symbols)
    volgistics_df['match_email'] = volgistics_df['email'].apply(clean_entries)
    volgistics_df['match_cell'] = volgistics_df['cell'].apply(clean_entries).apply(strip_symbols)
    volgistics_df['match_phone'] = volgistics_df['home'].apply(clean_entries).apply(strip_symbols)

    addr_components = [volgistics_df['street_1'], volgistics_df['street_2'], volgistics_df['street_3'], volgistics_df['city'], volgistics_df['state'], volgistics_df['zip'].fillna('').apply(str).str[:5]]
    volgistics_df['match_address_list'] = combine_address_columns(addr_components)
    #volgistics_df['match_address_list'] = volgistics_df['match_address_list'].apply(expand_address, languages=['en']).apply(json.dumps)

    load_to_sqlite(volgistics_df, 'volgistics', conn)

    # salesforce contacts
    sf_contacts_df = import_csv_and_clean_cols('../../sample_data/CfP_PDP_salesforceContacts_deidentified.csv', drop_first_col=True)

    sf_contacts_df['match_name'] = sf_contacts_df['last_name'].apply(clean_entries).apply(strip_symbols) + ' ' + sf_contacts_df['first_name'].apply(clean_entries).apply(strip_symbols)
    sf_contacts_df['match_email'] = sf_contacts_df['email'].apply(clean_entries)
    sf_contacts_df['match_cell'] = sf_contacts_df['mobile'].apply(clean_entries).apply(strip_symbols)
    sf_contacts_df['match_phone'] = sf_contacts_df['phone'].apply(clean_entries).apply(strip_symbols)

    addr_components = [sf_contacts_df['mailing_street'], sf_contacts_df['mailing_city'], sf_contacts_df['mailing_state_province'], sf_contacts_df['mailing_zip_postal_code'].fillna('').apply(str).str[:5]]
    sf_contacts_df['match_address_list'] = combine_address_columns(addr_components)
    #sf_contacts_df['match_address_list'] = sf_contacts_df['match_address_list'].apply(expand_address, languages=['en']).apply(json.dumps)

    load_to_sqlite(sf_contacts_df, 'salesforcecontacts', conn)

    # salesforce donations has account and opportunity id, but no personal information. 
    # I assume account_id maps to the account_id in salesforce contacts, so I'm cleaning column names and uploading the data as is
    sf_donations_df = import_csv_and_clean_cols('../../sample_data/CfP_PDP_salesforceDonations_deidentified.csv', drop_first_col=True)
    load_to_sqlite(sf_donations_df, 'salesforcedonations', conn)

    # close database connection
    conn.close()