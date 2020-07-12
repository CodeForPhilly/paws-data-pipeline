import datetime

from flask import current_app
from sqlalchemy import MetaData, Table, Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from config import engine

meta = MetaData(engine, reflect=True)


def start():
    if not engine.dialect.has_table(engine, 'petpoint'):
        current_app.logger.info('---------- Initiating DB -------------')
        Table('petpoint', meta,
              Column('animal_num', String),
              Column('outcome_person_num', String),
              Column('outcome_person_name', String),
              Column('out_street_address', String),
              Column('out_unit_number', Integer),
              Column('out_city', String),
              Column('out_province', String),
              Column('out_postal_code', String),
              Column('out_email', String),
              Column('out_home_phone', String),
              Column('out_cell_phone', String),
              Column('json', JSONB),
              Column('created_date', DateTime, default=datetime.datetime.utcnow),
              Column('archived_date', DateTime, default=None)
              )
        Table('volgistics', meta,
              Column('number', String),
              Column('last_name', String),
              Column('first_name', String),
              Column('middle_name', String),
              Column('complete_address', String),
              Column('street_1', String),
              Column('street_2', String),
              Column('street_3', String),
              Column('city', String),
              Column('state', String),
              Column('zip', String),
              Column('all_phone_numbers', String),
              Column('home', String),
              Column('work', String),
              Column('cell', String),
              Column('email', String),
              Column('json', JSONB),
              Column('created_date', DateTime, default=datetime.datetime.utcnow),
              Column('archived_date', DateTime, default=None)
              )
        Table('salesforcecontacts', meta,
              Column('contact_id', String),
              Column('first_name', String),
              Column('last_name', String),
              Column('mailing_street', String),
              Column('mailing_city', String),
              Column('mailing_state_province', String),
              Column('mailing_zip_postal_code', String),
              Column('phone', String),
              Column('mobile', String),
              Column('email', String),
              Column('json', JSONB),
              Column('created_date', DateTime, default=datetime.datetime.utcnow),
              Column('archived_date', DateTime, default=None)
              )
        Table('master', meta,
              Column('salesforcecontacts_id', String),
              Column('volgistics_id', String),
              Column('petpoint_id', String),
              Column('created_date', DateTime, default=datetime.datetime.utcnow),
              Column('archived_date', DateTime, default=None)
              )

        meta.create_all(engine)
