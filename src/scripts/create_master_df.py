import pandas as pd


def create_user_master_df(conn, table_name, query):
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
    df = pd.read_sql('select * from ' + table_name, conn)

    return df


def main(conn):
    # Create a simple table with the following values:
    # ------------> master_db_key, petpoint_id, volgistics_id, salesforce_id
    # petpoint[[outcome_person_id]]
    # volgistics[[volgistics_id]]
    # salesforcecontacts[[account_id]]

    # Create a new master_df table
    print('Start Creating master_df')
    master_df = create_user_master_df(
        conn, 'master_df',
        '(master_id INT PRIMARY KEY NOT NULL, petpoint_id text, volgistics_id text, salesforce_id text, email_address text )'
    )

    # Merge Petpoint data to the master_df
    # todo: add when petpoint is used
    # petpoint = pd.read_sql('select * from petpoint', conn)
    # master_df = petpoint[['outcome_person_id']].rename(
    #    columns={'outcome_person_id': 'petpoint_id', 'out_email': 'email_address'}).merge(master_df, how='left')

    # Merge Salesforce data to the master_df
    salesforcecontacts = pd.read_sql('select * from salesforcecontacts', conn)
    master_df.merge(salesforcecontacts[['account_id', 'email']].rename(
        columns={'account_id': 'salesforce_id'}), how='left')
    print('  -Successfully created salesforcecontact (Primary key) in master_df')

    # Merge Volgistics data into the master dataframe
    volgistics = pd.read_sql('select * from volgistics', conn)
    master_df.merge(volgistics[['number', 'email']].rename(columns={'email': 'email_address'}), how='left')
    print('  -Successfully created volgistics row in master_df')