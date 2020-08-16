import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Master(Base):
    __tablename__ = "master"

    _id = Column(Integer, primary_key=True)
    salesforcecontacts_id = Column(String)
    volgistics_id = Column(String)
    petpoint_id = Column(String)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    archived_date = Column(DateTime, default=None)


class User(Base):
    __tablename__ = "user_info"

    _id = Column(Integer, primary_key=True)
    master_id = Column(Integer)
    name = Column(String)
    email = Column(String)
    source = Column(String)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)

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

class Volgistics_Shifts(Base):
    __tablename__ = 'volgisticsshifts'

    _id = Column(Integer, primary_key=True)
    number = Column(String)
    site = Column(String)
    assignment = Column(String)
    from_date = Column(DateTime)
    to_date = Column(DateTime)
    from_time = Column(String)
    to_time = Column(String)
    hours = Column(Integer)
    no_call_no_show = Column(Integer)
    call_email_to_miss_shift = Column(Integer)
    absence = Column(Integer)

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
