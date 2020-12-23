import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
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


class SalesForceDonations(Base):
    __tablename__ = "salesforcedonations"

    _id = Column(Integer, primary_key=True)
    recurring_donor = Column(String)
    opportunity_owner = Column(String)
    account_id = Column(String)
    account_name = Column(String)
    opportunity_id = Column(String)
    opportunity_name = Column(String)
    stage = Column(String)
    fiscal_period = Column(String)
    amount = Column(String)
    probability = Column(String)
    age = Column(String)
    close_date = Column(String)
    created_date = Column(String)
    next_step = Column(String)
    lead_source = Column(String)
    type = Column(String)
    source = Column(String)
    contact_id = Column(String)
    primary_campaign_source = Column(String)


class Volgistics_Shifts(Base):
    __tablename__ = 'volgisticsshifts'

    _id = Column(Integer, primary_key=True)
    number = Column(String)
    site = Column(String)
    place = Column(String)
    assignment = Column(String)
    role = Column(String)
    from_date = Column('from', DateTime)
    to = Column(DateTime)
    spare_date = Column(String)
    spare_chechbox = Column(String)
    coordinator = Column(String)
