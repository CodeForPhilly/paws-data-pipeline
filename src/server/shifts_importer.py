import re
from flask.globals import current_app

from openpyxl import load_workbook
from jellyfish import jaro_similarity

from config import  engine

from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import  insert,  Table,  Column, MetaData, exc
from sqlalchemy.dialects.postgresql import Insert
metadata = MetaData()


MINIMUM_SIMILARITY = 0.85  # How good does the table match need to be?

expected_columns =  {
            'Number' : 'volg_id',
            'Site' : None,
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

def validate_import_vs(filename):
    """ Validate that the XLSX column names int the file are close enough to expectations that we can trust the data.
        If so, insert the data into the volgisticsshifts table. 
    """

    current_app.logger.info('---------------------- Loading ' + filename.filename  + '------------------------')
    wb = load_workbook(filename)   #  ,read_only=True should be faster but gets size incorrect 
    ws = wb.active   # Needs to be 'Service' sheet
    # ws.reset_dimensions()   # Tells openpyxl to ignore what sheet says and check for itself
    ws.calculate_dimension()