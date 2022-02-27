import pandas as pd
from models import PdpContacts, SalesForceContacts, ShelterluvPeople, Volgistics
from pipeline.flow_script import start_flow
from sqlalchemy import select
from sqlalchemy.orm import Session


def test_match(engine, session: Session, app):
    session.add_all(
        [
            SalesForceContacts(
                contact_id="abc123",
                first_name="Joe",
                last_name="Schmoe",
                mobile="5555555555",
                email="joe.schmoe@gmail.com",
            ),
            Volgistics(
                number="123456",
                first_name="Joe",
                last_name="Schmoe",
                email="joe.schmoe@gmail.com",
            ),
            ShelterluvPeople(
                internal_id="xyzabc",
                firstname="Schmoe",
                lastname="Joe and Amy",
                phone="5555555555",
            ),
            SalesForceContacts(
                contact_id="pqr789",
                first_name="Joe",
                last_name="Schmoe",
                mobile="6666666666",
            ),
        ]
    )
    session.commit()

    start_flow()

    expected_result = """\
   _id  matching_id         source_type source_id first_name    last_name
0    1            1  salesforcecontacts    abc123        Joe       Schmoe
1    2            2  salesforcecontacts    pqr789        Joe       Schmoe
2    3            1          volgistics    123456        Joe       Schmoe
3    4            1    shelterluvpeople    xyzabc     Schmoe  Joe and Amy"""
    assert pdp_contacts_string(engine) == expected_result


def pdp_contacts_string(engine):
    results = pd.read_sql_table(
        PdpContacts.__tablename__,
        engine,
        columns=[
            "_id",
            "matching_id",
            "source_type",
            "source_id",
            "first_name",
            "last_name",
        ],
    )
    return results.to_string()
