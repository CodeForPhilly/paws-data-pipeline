# import libraries
import sqlite3
import pandas as pd
import numpy as np
import re


# function for loading a csv into a database table or "updating" the table by dropping it and recreating it with the csv
def load_to_sqlite(csv_name, table_name, connection, drop_first_col=False, manual_index_name=None):
    # load csv into a dataframe
    df = pd.read_csv(csv_name, encoding='cp1252')

    # drop the first column - so far all csvs have had a first column that's an index and doesn't have a name
    if drop_first_col:
        df = df.drop(df.columns[0], axis=1)

    # strip whitespace and periods from headers, convert to lowercase
    df.columns = df.columns.str.lower().str.strip()
    df.columns = df.columns.str.replace(' ', '_')
    df.columns = df.columns.map(lambda x: re.sub(r'\.+', '_', x))

    # create a cursor object, and use it to drop the table if it exists
    cursor = connection.cursor()
    # if this table already exists, drop it
    df_table_name = pd.read_sql(
        '''SELECT name FROM sqlite_master WHERE type = "table" and name="''' + table_name + '''"''', connection)
    if not df_table_name.empty:
        cursor.execute(f'DROP TABLE {table_name}')
    connection.commit()
    cursor.close()

    # optionally add an ID number for linking against master data.
    # Ideally we would implement this feature by using sqlite's PRIMARY KEY constraint, but table schemas or
    # constraints cannot be modified in sqlite3 after they're defined.  The norm is altering the table name,
    # rebuilding the schema with the primary key constraint, then inserting all of the original data.
    if manual_index_name is not None:
        df[manual_index_name] = range(df.shape[0])

    # load dataframe into database table
    df.to_sql(table_name, connection, index=False, )


def create_user_master_df(connection, query):
    """
    Creates a pandas dataframe placeholder with key meta-data to fuzzy-match
    the users from different datasets.
    
    Pseudo-code:
        Create a blank pandas dataframe (e.g. pd.DataFrame) with columns for
        Name (last, first), address, zip code, phone number, email, etc.
        
        Include "ID" fields for each of the datasets that will be merged.
        
        Populate/Initialize the dataframe with data from one of the datasets
        (e.g. Salesforce)
    """

    # pull the dataframe from SQL database, call cleaning function, 
    # and add empty columns for the datasets that will be merged
    conn.execute('create table ' + table_name + ' ' + query)
    df = pd.read_sql('select * from ' + table_name, connection)

    return df


# connect to or create database
conn = sqlite3.connect("./paws_master_df.db")

# load data
# load petpoint
load_to_sqlite('./sample_data/CfP_PDP_petpoint_deidentified.csv', 'petpoint', conn, True)
# load volgistics
load_to_sqlite('./sample_data/CfP_PDP_volgistics_deidentified.csv', 'volgistics', conn, True, 'volgistics_id')
# load salesforce contacts
load_to_sqlite('./sample_data/CfP_PDP_salesforceContacts_deidentified.csv', 'salesforcecontacts', conn, True)
# load salesforce donations
load_to_sqlite('./sample_data/CfP_PDP_salesforceDonations_deidentified.csv', 'salesforcedonations', conn, True)

# Create a simple table with the following values:
# ------------> master_db_key, petpoint_id, volgistics_id, salesforce_id
#petpoint[[outcome_person_id]]
#volgistics[[volgistics_id]]
#salesforcecontacts[[account_id]]

# Create a new master_df table
master_df = create_user_master_df(conn, 'master_df', '(master_id INT PRIMARY KEY NOT NULL, petpoint_id text, volgistics_id text, salesforce_id text, email_address text )')

# Merge Petpoint data to the master_df
master_df = petpoint[['outcome_person_id']].rename(columns={'outcome_person_id': 'petpoint_id', 'out_email' : 'email_address'}).merge(master_df, how='left')
        
# Merge Salesforce data to the master_df
master_df.merge(salesforcecontacts[['account_id', 'email']].rename(columns={'account_id' : 'salesforce_id' }), how='left')

# Merge Volgistics data into the master dataframe
master_df = volgistics[['volgistics_id', 'email']].rename(columns={'email' : 'email_address'}).merge(master_df, how='left')
