import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Master(Base):
    __tablename__ = "master"

    _id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    salesforcecontacts_id = Column(String)
    volgistics_id = Column(String)
    petpoint_id = Column(String)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    archived_date = Column(DateTime, default=None)

class SalesForceContacts(Base):
    __tablename__ = "salesforcecontacts"

    _id = Column(Integer, primary_key=True)
    contact_id = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    mailing_street = Column(String)
    mailing_city = Column(String)
    mailing_state_province = Column(String)
    mailing_zip_postal_code = Column(String)
    phone = Column(String)
    mobile = Column(String)
    email = Column(String)
    json = Column(JSONB)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    archived_date = Column(DateTime, default=None)

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
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    archived_date = Column(DateTime, default=None)

class Petpoint(Base):
    __tablename__ = "petpoint"

    _id = Column(Integer, primary_key=True)
    animal_num = Column(String)
    outcome_person_num = Column(String)
    outcome_person_name = Column(String)
    out_street_address = Column(String)
    out_unit_number = Column(String)
    out_city = Column(String)
    out_province = Column(String)
    out_postal_code = Column(String)
    out_email = Column(String)
    out_home_phone = Column(String)
    out_cell_phone = Column(String)
    json = Column(JSONB)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    archived_date = Column(DateTime, default=None)
