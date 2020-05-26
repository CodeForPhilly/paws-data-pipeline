import pandas as pd
import re

from config import engine
from flask import current_app


# function for loading a csv into a database table or "updating" the table by dropping it and recreating it with the csv
def load_to_postgres(csv_path, table_name, drop_first_col=False):
    # connect to or create database
    # load csv into a dataframe
    df = pd.read_csv(csv_path, encoding='cp1252')
    
    # drop the first column - so far all csvs have had a first column that's an index and doesn't have a name
    if drop_first_col:
        df = df.drop(df.columns[0], axis=1)
    
    # strip whitespace and periods from headers, convert to lowercase
    df.columns = df.columns.str.lower().str.strip()
    df.columns = df.columns.str.replace(' ', '_')
    df.columns = df.columns.map(lambda x: re.sub(r'\.+', '_', x))
    #temp table
    df.to_sql(table_name + '_temp', engine, index=False, if_exists='replace')
    
    
    # get conneciton from engine and use in with clause to automatically handle transaction cleanup
    '''with engine.connect() as connection:
        connection.execute(f'DROP TABLE IF EXISTS {table_name}')
        # load dataframe into database table
        current_app.logger.info('Creating table: ' + table_name)
        df.to_sql(table_name, engine, index=False,)
        current_app.logger.info('Finished creating generic table for: ' + table_name)'''

def find_new_rows():
    with engine.connect() as connection:
        rows = connection.execute(f'select * from volgistics_temp left join volgistics v on v.number = t.number where v.number is null')
        for row in rows:

