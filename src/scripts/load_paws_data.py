import sqlalchemy as db
import pandas as pd
import re

from config import DB
from flask import current_app

engine = db.create_engine(DB)


# function for loading a csv into a database table or "updating" the table by dropping it and recreating it with the csv
def load_to_postgres(csv_path, table_name, drop_first_col=False):
    # connect to or create database
    connection = engine.raw_connection()
    # load csv into a dataframe
    df = pd.read_csv(csv_path, encoding='cp1252')
    
    # drop the first column - so far all csvs have had a first column that's an index and doesn't have a name
    if drop_first_col:
        df = df.drop(df.columns[0], axis=1)
    
    # strip whitespace and periods from headers, convert to lowercase
    df.columns = df.columns.str.lower().str.strip()
    df.columns = df.columns.str.replace(' ', '_')
    df.columns = df.columns.map(lambda x: re.sub(r'\.+', '_', x))
    
    # create a cursor object, and use it to drop the table if it exists
    cursor = connection.cursor()
    cursor.execute(f'DROP TABLE IF EXISTS {table_name}')
    connection.commit()
    cursor.close()
    
    # load dataframe into database table
    current_app.logger.info('Creating table: ' + table_name)
    df.to_sql(table_name, engine, index=False,)
    current_app.logger.info('Finished creating generic table for: ' + table_name)
    return engine  # pandas is expecting a db.Engine object instead of the raw_connection