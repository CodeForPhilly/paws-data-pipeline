import re


def __clean_csv_headers(header):
    header = re.sub(r'\s\(.*\)', '', header)
    header = re.sub(r'\.+', '_', header.lower().strip().replace(' ', '_').replace('/', '_'))
    return header.replace('#', 'num')


CSV_HEADERS = {
    'shelterluvpeople': ['Firstname', 'Lastname', 'ID', 'Internal-ID', 'PreviousIds', 'Associated', 'Street',
                         'Apartment', 'City', 'State', 'Zip', 'Email', 'Phone', 'Animal_ids'],
    'volgistics': ['Last name', 'First name', 'Middle name', 'Number', 'Complete address', 'Street 1', 'Street 2',
                   'Street 3', 'City', 'State', 'Zip', 'All phone numbers', 'Home', 'Work', 'Cell', 'Email'],
    'salesforcecontacts': ['Contact ID', 'First Name', 'Last Name', 'Mailing Street', 'Mailing City',
                           'Mailing State/Province', 'Mailing Zip/Postal Code', 'Mailing Country', 'Phone', 'Mobile',
                           'Email'],
    'volgisticsshifts': ['Number', 'Site', 'Place', 'Assignment', 'Role', 'From', 'To', 'Spare date', 'Spare dropdown',
                         'Spare checkbox', 'Coordinator'],
    'salesforcedonations': ['Recurring donor', 'Opportunity Owner', 'Account Name', 'Opportunity ID (18 Digit)',
                            'Account ID (18 digit)',
                            'Opportunity Name', 'Stage', 'Fiscal Period', 'Amount', 'Probability (%)', 'Age',
                            'Close Date', 'Created Date', 'Type', 'Primary Campaign Source',
                            'Source', 'Contact ID (18 Digit)', 'Primary Contact']
}

DATASOURCE_MAPPING = {
    'salesforcecontacts': {
        'id': 'contact_id',
        'csv_names': CSV_HEADERS['salesforcecontacts'],
        'tracked_columns': list(map(__clean_csv_headers, CSV_HEADERS['salesforcecontacts'])),
        'table_email': 'email',
        '_table_name': ['first_name', 'last_name'],
        'should_drop_first_column': True
    },
    'volgistics': {
        'id': 'number',
        'csv_names': CSV_HEADERS['volgistics'],
        'tracked_columns': list(map(__clean_csv_headers, CSV_HEADERS['volgistics'])),
        'table_email': 'Email'.lower(),
        '_table_name': ['first_name', 'last_name'],
        'sheetname': 'Master',
        'should_drop_first_column': True
    },
    'shelterluvpeople': {
        'id': 'id',
        'csv_names': CSV_HEADERS['shelterluvpeople'],
        'tracked_columns': list(map(__clean_csv_headers, CSV_HEADERS['shelterluvpeople'])),
        'table_email': 'Email'.lower(),
        '_table_name': ['Firstname'.lower(), 'Lastname'.lower()],
        'should_drop_first_column': False
    },
    'volgisticsshifts': {
        'id': 'number',
        'csv_names': CSV_HEADERS['volgisticsshifts'],
        'tracked_columns': list(map(__clean_csv_headers, CSV_HEADERS['volgisticsshifts'])),
        'table_email': None,
        '_table_name': None,
        'sheetname': 'Assignments',
        'should_drop_first_column': True
    },
    'salesforcedonations': {
        'id': 'contact_id',
        'csv_names': CSV_HEADERS['salesforcedonations'],
        'tracked_columns': list(map(__clean_csv_headers, CSV_HEADERS['salesforcedonations'])),
        'table_email': None,
        '_table_name': None,
        'should_drop_first_column': True
    }
}


def volgistics_address(index, street):
    result = ""

    for item in street:
        if isinstance(item, str):
            if " " in item:
                result = item.split()[index]

    return result


def normalize_phone_number(number):
    result = None

    if number and str(number) != 'nan':
        number = re.sub('[() -.+]', '', number)

        if number[0] == '1':
            number = number[1:]

        if number.isdigit() and len(number) == 10:
            result = number
        else:
            print("Invalid phone number was not loaded: " + number)

    return result


SOURCE_NORMALIZATION_MAPPING = {
    "salesforcecontacts": {
        "source_id": "contact_id",
        "first_name": "first_name",
        "last_name": "last_name",
        "email": "email",
        "mobile": lambda df: df["mobile"].combine_first(df["phone"]).apply(normalize_phone_number),
        "street_and_number": "mailing_street",
        "apartment": "mailing_street",
        "city": "mailing_city",
        "state": "mailing_state_province",
        "zip": "mailing_zip_postal_code",
        "others": {
            "should_drop_first_column": True
        }

    },
    "salesforcedonations": {
        "parent": "salesforcecontacts",
        "others": {
            "should_drop_first_column": True
        }
    },
    "shelterluvpeople": {
        "source_id": "internal-id",
        "first_name": "firstname",
        "last_name": "lastname",
        "email": "email",
        "mobile": lambda df: df["phone"].apply(normalize_phone_number),
        "street_and_number": "street",
        "apartment": "apartment",
        "city": "city",
        "state": "state",
        "zip": "zip",
        "others": {
            "should_drop_first_column": False
        }
    },
    "volgistics": {
        "source_id": "number",
        "first_name": "first_name",
        "last_name": "last_name",
        "email": "email",
        "mobile": lambda df: df["cell"].combine_first(df["home"]).apply(normalize_phone_number),
        "street_and_number": lambda df: volgistics_address(1, df["street_1"]),
        "apartment": lambda df: volgistics_address(0, df["street_1"]),
        "city": "city",
        "state": "state",
        "zip": "zip",
        "others": {
            "should_drop_first_column": True
        }
    },
    "volgisticsshifts": {
        "parent": "volgistics",
        "others": {
            "should_drop_first_column": True
        }
    }
}
