import re
from flask.globals import current_app

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

        # Stats for import
        dupes = 0
        other_integrity = 0
        other_exceptions = 0
        row_count = 0
        missing_contact_id = 0

        for row in ws.values:        
            if seen_header: 
                row_count += 1
                if row_count % 1000 == 0:
                    current_app.logger.info("Row: " + str(row_count) )
                zrow = dict(zip(expected_columns.values(), row))  
                # zrow is a dict of db_col:value pairs, with at most one key being None (as it overwrote any previous)
                # We need to remove the None item, if it exists
                try:
                    del zrow[None]
                except KeyError:
                    pass 

                #  Cleanup time!  Many older imports have... peculiarities 
                if zrow['amount'] == None:  # We get some with no value, probably user error
                    zrow['amount'] = 0.0    # Setting bad amounts to 0 as per KF

                if zrow['recurring_donor'] == '=FALSE()' :
                    zrow['recurring_donor'] = False

                if zrow['recurring_donor'] == '=TRUE()' :
                    zrow['recurring_donor'] = True

                #  End cleanup 

                if zrow['contact_id'] :  # No point in importing if there's nothing to match
                    # Finally ready to insert row into the table
                    # 
                    stmt = insert(sfd).values(zrow).execution_options(synchronize_session="fetch")
                    try:
                        result = session.execute(stmt)
                    except exc.IntegrityError as e:  # Catch-all for several more specific exceptions
                        if  re.match('duplicate key value', str(e.orig) ):
                            dupes += 1
                            pass
                        else:
                            other_integrity += 1
                            print(e)
                    except Exception as e: 
                        other_exceptions += 1
                        print(e)

                    session.commit()   # If performance is bad, we may need to batch
                else: # Missing contact_id
                    missing_contact_id += 1


            else:  # Haven't seen header, so this was first row.
                seen_header = True

        current_app.logger.info("---------------------------------   Stats -------------------------------------------------")
        current_app.logger.info("Total rows: " + str(row_count) + " Dupes: " + str(dupes) + " Missing contact_id: " + str(missing_contact_id) )
        current_app.logger.info("Other integrity exceptions: " + str(other_integrity) + " Other excptions: " + str(other_exceptions) )
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
