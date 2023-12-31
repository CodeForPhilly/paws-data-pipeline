import os

import structlog
from simple_salesforce import Salesforce
from sqlalchemy.orm import sessionmaker

from config import engine
from models import SalesForceContacts

from api import pem

logger = structlog.get_logger()

TEST_MODE = os.getenv("TEST_MODE")  # if not present, has value None

DOMAIN = os.getenv("SALESFORCE_DOMAIN")
CONSUMER_KEY = os.getenv('SALESFORCE_CONSUMER_KEY')
USERNAME = os.getenv('SALESFORCE_USERNAME')

def store_contacts_all():
    Session = sessionmaker(engine)
    with Session() as session:

        logger.debug("truncating table salesforcecontacts")
        session.execute("TRUNCATE TABLE salesforcecontacts")

        logger.debug("retrieving the latest salesforce contacts data")

        pem_file = pem.find_pem_file()

        if pem_file == '':
            logger.error("Missing salesforce jwt private key pem file, skipping data pull")
            return


        sf = Salesforce(username=USERNAME, consumer_key=CONSUMER_KEY,
                        privatekey_file=pem_file, domain=DOMAIN)
        results = sf.query("SELECT Contact_ID_18__c, FirstName, LastName, Contact.Account.Name, MailingCountry, MailingStreet, MailingCity, MailingState, MailingPostalCode, Phone, MobilePhone, Email FROM Contact")
        logger.debug("%d total Salesforce contact records", results['totalSize'])
        if TEST_MODE:
            logger.debug("running in test mode so only downloading first page of Salesforce contacts")

        total_records = 0
        done = False
        while not done:
            total_records += len(results['records'])
            logger.debug("Query returned %d Salesforce contact records, total %d", len(results['records']), total_records)
            for row in results['records']:
                account_name = row['Account']['Name'] if row['Account'] is not None else None
                contact = SalesForceContacts(contact_id=row['Contact_ID_18__c'],
                                             first_name=row['FirstName'],
                                             last_name=row['LastName'],
                                             account_name=account_name,
                                             mailing_country=row['MailingCountry'],
                                             mailing_street=row['MailingStreet'],
                                             mailing_city=row['MailingCity'],
                                             mailing_state_province=row['MailingState'],
                                             mailing_zip_postal_code=row['MailingPostalCode'],
                                             phone=row['Phone'],
                                             mobile=row['MobilePhone'],
                                             email=row['Email'])
                session.add(contact)
            # if in test mode only return first page of results
            done = results['done'] if not TEST_MODE else True
            if not done:
                results = sf.query_more(results['nextRecordsUrl'], True)
        logger.debug("Committing downloaded contact records")
        session.commit()
    logger.info("finished downloading latest salesforce contacts data")
