from openpyxl import load_workbook
from jellyfish import jaro_similarity

from config import  engine

from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import  insert,  Table,  Column, MetaData, exc

metadata = MetaData()



MINIMUM_SIMILARITY = 0.85  # How good does the table match need to be?

expected_columns =  {'Recurring donor' : 'recurring_donor',        # 'Export XLSX file column name' : 'db column name' 
                    'Opportunity Owner': None ,                    # None means we won't import that column into DB
                    'Account ID 18': None ,
                    'Account Name':  None, 
                    'Primary Contact': 'primary_contact',
                    'Contact ID 18': 'contact_id',
                    'Opportunity ID 18': 'opp_id',   # Should be a unique donation ID but isn't quite
                    'Opportunity Name': None,
                    'Stage': None,
                    'Fiscal Period': None, 
                    'Amount': 'amount', 
                    'Probability (%)': None, 
                    'Age': None,
                    'Close Date': 'close_date', 
                    'Created Date': None, 
                    'Type': 'donation_type', 
                    'Primary Campaign Source': 'primary_campaign_source' ,
                    'Source': None }
                    

def validate_import_sfd(filename):
    """ Validate that the XLSX column names int the file are close enough to expectations that we can trust the data.
        If so, insert the data into the salseforcedonations table. 
    """

    print('******************** Loading ' + filename.filename )
    wb = load_workbook(filename)   #  ,read_only=True should be faster but gets size incorrect 
    ws = wb.active
    # ws.reset_dimensions()   # Tells openpyxl to ignore what sheet says and check for itself
    ws.calculate_dimension()

    columns = ws.max_column
    if columns > 26:
        print("Sorry, I only handle A-Z columns") # TODO: Handle AA, AB, usw...
        columns = 26

    header = [cell.value for cell in ws[1]]

    min_similarity = 1.0
    min_column = None

    for expected, got in zip(expected_columns.keys(), header):
        jsim = jaro_similarity(expected, got) 
        if jsim < min_similarity :
            min_similarity = jsim
            min_column = expected + ' / ' + got
    
    

    print("Minimum similarity: {:.2}".format(min_similarity) )
    if min_column:
        print("On expected/got: ", min_column)

    if  min_similarity >= MINIMUM_SIMILARITY :  # Good enough to trust
        
        Session = sessionmaker(engine) 
        session =  Session()   
        sfd  = Table("salesforcedonations", metadata, autoload=True, autoload_with=engine)

        seen_header = False  # Used to skip header row

        for row in ws.values:        
            if seen_header: 
                zrow = dict(zip(expected_columns.values(), row))  
                # zrow is a dict of db_col:value pairs, with at most one key being None (as it overwrote any previous)
                # We need to remove the None item, if it exists
                try:
                    del zrow[None]
                except KeyError:
                    pass 

                #    if zrow['primary_contact'] != 'Missing First Name Missing Last Name' : # No reason to import these, but it's not going to hurt anything
                if zrow['amount'] == None:  # We get some with no value, probably user error
                    zrow['amount'] = 0.0    # Setting bad amounts to 0 as per KF

                # Finally ready to insert row into the table
                # 
                stmt = insert(sfd).values(zrow).execution_options(synchronize_session="fetch")
                try:
                    result = session.execute(stmt)
                except exc.IntegrityError as e:
                    print(e)

                session.commit()   # If performance is bad, we may need to batch


            else:  # Haven't seen header, so this was first row.
                seen_header = True


        session.close()
        wb.close()
        return { True : "File imported" }

    else:  # Similarity too low 
        wb.close()
        return {False : "Similarity to expected column names below threshold"}






if __name__ == "__main__":

    path = "C:\\Dropbox\\PAWS PDP\\latest raw data\\"
    filenames = [   
                "Salesforce_PAWS Donation_9_1_2020_TO_6_10_2021_unedited.xlsx",
                "Salesforce_PAWS Donation_3_29_2021_TO_6_1_2021.xlsx",
                "Salesforce_PAWS Donation_9_1_2020_TO_3_30_2021.xlsx",
                "Salesforce_PAWS Donation (all Time) (excel).xlsx", 
                "Copy_of_Salesforce_PAWS Donation (all Time) 2021-06-15.xlsx",
                "Salesforce_PAWS Donation (all Time) 2021-06-15.xlsx"
                ]


    validate_import_sfd(path + filenames[0])
