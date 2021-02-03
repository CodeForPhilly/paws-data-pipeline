import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Master(Base):
    __tablename__ = "master"

    _id = Column(Integer, primary_key=True)
    salesforcecontacts_id = Column(String, default=None)
    volgistics_id = Column(String, default=None)
    shelterluvpeople_id = Column(String, default=None)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    archived_date = Column(DateTime, default=None)


class User(Base):
    __tablename__ = "user_info"

    _id = Column(Integer, primary_key=True)
    master_id = Column(Integer, ForeignKey("master._id"))
    name = Column(String)
    email = Column(String)
    source = Column(String)
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
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    archived_date = Column(DateTime, default=None)


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

