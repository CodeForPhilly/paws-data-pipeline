import os

from sqlalchemy.orm import  sessionmaker
from simple_salesforce import Salesforce
from config import engine
from models import SalesForceContacts

import structlog
logger = structlog.get_logger()

def store_contacts_all():
    Session = sessionmaker(engine)
    with Session() as session:

        logger.debug("truncating table salesforcecontacts")
        session.execute("TRUNCATE TABLE salesforcecontacts")

        logger.debug("retrieving the latest salesforce contacts data")
        sf = Salesforce(domain=os.getenv('SALESFORCE_DOMAIN'), password=os.getenv('SALESFORCE_PW'), username=os.getenv('SALESFORCE_USERNAME'), security_token=os.getenv('SALESFORCE_SECURITY_TOKEN'))
        results = sf.query("SELECT Contact_ID_18__c, FirstName, LastName, Contact.Account.Name, MailingCountry, MailingStreet, MailingCity, MailingState, MailingPostalCode, Phone, MobilePhone, Email FROM Contact")
        logger.debug("Query returned %d Salesforce contact records", len(results['records']) )
        
        done = False
        while not done:
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
                                             email=['Email'])
                session.add(contact)
                done = results['done']
                if not done:
                    results = sf.query_more(results['nextRecordsUrl'])
        session.commit()
    logger.debug("finished downloading latest salesforce contacts data")