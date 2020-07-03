#from flask import current_app
import re

def __clean_csv_headers(header):
    header =  re.sub(r'\.+', '_', header.lower().strip().replace(' ', '_'))
    return header.replace('#','num')

CSV_HEADERS = {
    'petpoint': ['Animal #', 'Outcome Person #', 'Outcome Person Name', 'Out Street Address', 'Out Unit Number', 'Out City', 'Out Province', 'Out Postal Code', 'Out Email', 'Out Home Phone', 'Out Cell Phone'],
    'volgistics': ['Last name', 'First name', 'Middle name', 'Number', 'Complete address', 'Street 1', 'Street 2', 'Street 3', 'City', 'State', 'Zip', 'All phone numbers', 'Home', 'Work', 'Cell', 'Email'],
    'salesforcecontacts': ['Contact ID', 'First Name', 'Last Name', 'Mailing Street', 'Mailing City', 'Mailing State/Province', 'Mailing Zip/Postal Code', 'Mailing Country', 'Phone', 'Mobile', 'Email']
}

DATASOURCE_MAPPING = {
    'salesforcecontacts': {
        'id': 'contact_id',
        'csv_names': CSV_HEADERS['salesforcecontacts'],
        'tracked_columns': list(map(__clean_csv_headers, CSV_HEADERS['salesforcecontacts'])),
        'identifying_criteria': []
    },
    'volgistics': {
        'id': 'number',
        'csv_names': CSV_HEADERS['volgistics'],
        'tracked_columns': list(map(__clean_csv_headers, CSV_HEADERS['volgistics'])),
        'identifying_criteria': []
    },
    'petpoint': {
        'id': 'animal_num',
        'csv_names': CSV_HEADERS['petpoint'],
        'tracked_columns': list(map(__clean_csv_headers, CSV_HEADERS['petpoint'])),
        'identifying_criteria': []
    }
}