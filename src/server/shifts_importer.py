import re
from flask.globals import current_app

from openpyxl import load_workbook
from jellyfish import jaro_similarity

from config import  engine

import structlog
logger = structlog.get_logger()


from sqlalchemy import  insert,  Table,  Column, MetaData, exc
from sqlalchemy.dialects.postgresql import Insert
metadata = MetaData()


MINIMUM_SIMILARITY = 0.85  # How good does the table match need to be?

expected_columns =  {
            'Number' : 'volg_id',
            'Site' : 'site',
            'Place' : None,
            'Assignment' : 'assignment',
            'From date' : 'from_date',
            'To date' : None,
            'From time' :None,
            'To time' : None,
            'Hours' : 'hours',
            'No Call/No Show' : None,
            'Call/Email to miss shift' : None,
            'Absence' : None,
            'Volunteers' : None
            }

def validate_import_vs(filename, conn):
    """ Validate that the XLSX column names int the file are close enough to expectations that we can trust the data.
        If so, insert the data into the volgisticsshifts table. 
    """

    logger.info('------ Loading %s ',  filename.filename )
    wb = load_workbook(filename)   #  ,read_only=True should be faster but gets size incorrect 
    ws = wb['Service']   # Needs to be 'Service' sheet
    # ws.reset_dimensions()   # Tells openpyxl to ignore what sheet says and check for itself
    ws.calculate_dimension()

    columns = ws.max_column
    if columns > 26:
        # TODO: Handle AA, AB, usw...
        logger.warn("Column count > 26; columns after Z not processed")
        columns = 26

    header = [cell.value for cell in ws[1]]

    min_similarity = 1.0
    min_column = None

    for expected, got in zip(expected_columns.keys(), header):
        jsim = jaro_similarity(expected, got) 
        if jsim < min_similarity :
            min_similarity = jsim
            min_column = expected + ' / ' + got

        
    logger.debug("Minimum similarity:  %s", "{:.2}".format(min_similarity) )
    if min_column:
        logger.debug("On expected/got: %s", str(min_column))


    if  min_similarity >= MINIMUM_SIMILARITY :  # Good enough to trust
        
        vs  = Table("volgisticsshifts", metadata, autoload=True, autoload_with=engine)

        seen_header = False  # Used to skip header row

        # Stats for import
        dupes = 0
        other_integrity = 0
        other_exceptions = 0
        row_count = 0
        missing_volgistics_id = 0

        for row in ws.values:        
            if seen_header: 
                row_count += 1
                if row_count % 1000 == 0:
                    logger.debug("Row: %s", str(row_count) )
                zrow = dict(zip(expected_columns.values(), row))  
                # zrow is a dict of db_col:value pairs, with at most one key being None (as it overwrote any previous)
                # We need to remove the None item, if it exists
                try:
                    del zrow[None]
                except KeyError:
                    pass 

                #  Cleanup time!  Many older imports have... peculiarities 

                #  End cleanup 

                if zrow['volg_id'] :  # No point in importing if there's nothing to match
                    # Finally ready to insert row into the table
                    # 

                    stmt = Insert(vs).values(zrow)

                    skip_dupes = stmt.on_conflict_do_nothing(
                        constraint='uq_shift'
                       )
                    try:
                        result = conn.execute(skip_dupes)
                    except exc.IntegrityError as e:  # Catch-all for several more specific exceptions
                        if  re.match('duplicate key value', str(e.orig) ):
                            dupes += 1
                            pass
                        else:
                            other_integrity += 1
                            logger.error(e)
                    except Exception as e: 
                        other_exceptions += 1
                        logger.error(e)
                 
                else: # Missing contact_id
                    missing_volgistics_id += 1


            else:  # Haven't seen header, so this was first row.
                seen_header = True

        # NOTE: we now run this in a engine.begin() context manager, so our
        # parent will commit. Don't commit here!


        logger.info("Total rows: %s  Dupes: %s Missing volgistics id: %s",  str(row_count), str(dupes), str(missing_volgistics_id)  )
        logger.info("Other integrity exceptions: %s  Other exceptions: %s",  str(other_exceptions),  str(other_integrity) )
        wb.close()
        return { True : "File imported" }