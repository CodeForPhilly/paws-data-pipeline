import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class PdpContacts(Base):
    __tablename__ = "pdp_contacts"

    _id = Column(Integer, primary_key=True, autoincrement=True)
    matching_id = Column(Integer)
    source_type = Column(String)
    source_id = Column(String)
    first_name = Column(String, default=None)
    last_name = Column(String, default=None)
    email = Column(String, default=None)
    mobile = Column(String, default=None)
    street_and_number = Column(String, default=None)
    apartment = Column(String)
    city = Column(String, default=None)
    state = Column(String, default=None)
    zip = Column(String, default=None)
    json = Column(JSONB)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    archived_date = Column(DateTime, default=None)



class SalesForceContacts(Base):
    __tablename__ = "salesforcecontacts"

    _id = Column(Integer, primary_key=True)
    contact_id = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    mailing_country = Column(String)
    mailing_street = Column(String)
    mailing_city = Column(String)
    mailing_state_province = Column(String)
    mailing_zip_postal_code = Column(String)
    phone = Column(String)
    mobile = Column(String)
    email = Column(String)
    json = Column(JSONB)


class ShelterluvPeople(Base):
    __tablename__ = "shelterluvpeople"

    _id = Column(Integer, primary_key=True)
    firstname = Column(String)
    lastname = Column(String)
    id = Column(String)
    associated = Column(String)
    street = Column(String)
    apartment = Column(String)
    city = Column(String)
    state = Column(String)
    zip = Column(String)
    email = Column(String)
    phone = Column(String)
    animal_ids = Column(JSONB)
    json = Column(JSONB)


class Volgistics(Base):
    __tablename__ = "volgistics"

    _id = Column(Integer, primary_key=True)
    number = Column(String)
    last_name = Column(String)
    first_name = Column(String)
    middle_name = Column(String)
    complete_address = Column(String)
    street_1 = Column(String)
    street_2 = Column(String)
    street_3 = Column(String)
    city = Column(String)
    state = Column(String)
    zip = Column(String)
    all_phone_numbers = Column(String)
    home = Column(String)
    work = Column(String)
    cell = Column(String)
    email = Column(String)
    json = Column(JSONB)

