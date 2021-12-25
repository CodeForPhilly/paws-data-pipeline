from api.api import common_api
from config import engine
from flask import jsonify, current_app
from sqlalchemy.sql import text
import requests
import time
from datetime import datetime

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import Table, MetaData
from pipeline import flow_script
from config import engine
from flask import request, redirect, jsonify, current_app
from api.file_uploader import validate_and_arrange_upload
from sqlalchemy.orm import Session, sessionmaker


def insert_animals(animal_list):
    """Insert animal records into shelterluv_animals table and return row count. """

    Session = sessionmaker(engine)
    session = Session()
    metadata = MetaData()
    sla = Table("shelterluv_animals", metadata, autoload=True, autoload_with=engine)

    # From Shelterluv: ['ID',       'Internal-ID', 'Name', 'Type', 'DOBUnixTime', 'CoverPhoto', 'LastUpdatedUnixTime']
    # In db:           ['local_id', 'id' (PK),     'name', 'type', 'dob',         'photo',      'update_stamp']

    ins_list = []  # Create a list of per-row dicts
    for rec in animal_list:
        ins_list.append(
            {
                "id": rec["Internal-ID"],
                "local_id": rec["ID"] if rec["ID"] else 0,  # Sometimes there's no local id
                "name": rec["Name"],
                "type": rec["Type"],
                "dob": rec["DOBUnixTime"],
                "update_stamp": rec["LastUpdatedUnixTime"],
                "photo": rec["CoverPhoto"],
            }
        )

    ret = session.execute(sla.insert(ins_list))

    session.commit()  # Commit all inserted rows
    session.close()

    return ret.rowcount
