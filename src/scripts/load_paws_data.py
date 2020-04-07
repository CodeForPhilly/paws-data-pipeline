import sqlite3
import sqlalchemy as db
import pandas as pd
import numpy as np
import re
from fuzzywuzzy import fuzz

# connect to or create database

engine = db.create_engine('postgresql://postgres:thispasswordisverysecure@paws-compose-db/postgres')
conn = engine.raw_connection()
# function for loading a csv into a database table or "updating" the table by dropping it and recreating it with the csv
OUTPUT_PATH = "/app/static/output/"

def load_to_sqlite(csv_name, table_name, connection, engine, drop_first_col=False):
    
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
    try:
        cursor.execute(f'DROP TABLE {table_name}')
    except:
        # Petpoint DB does not already exist
        pass
    connection.commit()
    cursor.close()
    
    # load dataframe into database table
    df.to_sql(table_name, engine, index=False,)

#load_to_sqlite(UPLOADED_FILES_PATH + '/CfP_PDP_petpoint_deidentified.csv', 'petpoint', conn, True)
#load_to_sqlite(UPLOADED_FILES_PATH + '/CfP_PDP_volgistics_deidentified.csv', 'volgistics', conn, True)
#load_to_sqlite(UPLOADED_FILES_PATH + '/CfP_PDP_salesforceContacts_deidentified.csv', 'salesforcecontacts', conn, True)
#load_to_sqlite(UPLOADED_FILES_PATH + '/CfP_PDP_salesforceDonations_deidentified.csv', 'salesforcedonations', conn, True)