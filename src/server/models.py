import datetime
import re
from itertools import combinations

import pandas as pd
import sqlalchemy as sa
from sqlalchemy import (
    Boolean,
    DateTime,
    Index,
    Integer,
    String,
    delete,
    desc,
    func,
    literal_column,
    select,
    text,
    tuple_,
)
from sqlalchemy.dialects.postgresql import JSONB, insert
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.functions import coalesce

Base = declarative_base()


def Column(*colargs, source_column=None, contacts_column=None, **kwargs):
    # Currently many of our database tables are populated by loading some csv or
    # excel table and inserting those columns with little more than a column
    # name change. Many of those databse columns will also later be copied into
    # pdp_contacts with little processing. This drop-in replacement for
    # sqlalchemy's Column function lets us easily provide this extra information
    # for some automated processing.

    info = kwargs.get("info", {})
    if source_column:
        info["source_column"] = source_column
    if contacts_column:
        info["contacts_column"] = contacts_column

    return sa.Column(*colargs, info=info, **kwargs)


def get_source_column_translation(cls):
    # Produce a mapping of source column to database column for a class that
    # uses the Column helper

    return {
        col.info["source_column"]: col.name
        for col in cls.__table__.columns
        if "source_column" in col.info
    }


def get_contacts_mapping(cls):
    # Produce an association of pdp_contacts columns with some other table's
    # columns for use in an INSERT ... FROM SELECT

    return [
        (PdpContacts.matching_id, 0),
        (PdpContacts.source_type, literal_column(f"'{cls.__tablename__}'")),
    ] + [
        (col.info["contacts_column"], col)
        for col in cls.__table__.columns
        if "contacts_column" in col.info
    ]


def dedup_consecutive(table, unique_id, id, order_by, dedup_on):
    # Many of our raw data tables have a similar structure: a contact id column,
    # an insert time column, and several other pieces of raw data. If someone
    # inserts a "new" record for a certain id, but none of the raw data is
    # different from the previous record, we'd like to get rid of it.
    #
    # This bit of SQL magic partitions a table by a given id column, orders it
    # by some order_by column, and removes duplicate consecutive entries based
    # on some dedup_on expression.
    #
    # Note the use of "IS NOT DISTINCT FROM" instead of "!="; the latter does
    # not work well on null values.

    sq = select(
        unique_id,
        id,
        order_by,
        dedup_on.bool_op("IS NOT DISTINCT FROM")(
            func.lag(dedup_on).over(partition_by=id, order_by=order_by)
        ).label("is_dupe"),
    ).subquery()

    to_delete = select(sq.c[0]).where(sq.c[3]).subquery()
    return delete(table).where(unique_id == to_delete.c[0])


def normalize_phone_number(number):
    result = None

    if number and str(number) != "nan":
        number = re.sub("[() -.+]", "", str(number))

        if number and number[0] == "1":
            number = number[1:]

        if number.isdigit() and len(number) == 10:
            result = number

    return result


class PdpContacts(Base):
    __tablename__ = "pdp_contacts"
    __table_args__ = (
        Index("idx_pdp_contacts_lower_first_name", text("lower(first_name)")),
        Index("idx_pdp_contacts_lower_last_name", text("lower(last_name)")),
        Index("idx_pdp_contacts_lower_email", text("lower(email)")),
        Index("idx_pdp_contacts_source_type_and_id", "source_type", "source_id"),
    )

    _id = Column(Integer, primary_key=True, autoincrement=True)
    matching_id = Column(Integer)
    source_type = Column(String)
    source_id = Column(String)
    is_organization = Column(Boolean, default=False)
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


P = PdpContacts


class SalesForceContacts(Base):
    __tablename__ = "salesforcecontacts"

    _id = Column(Integer, primary_key=True)
    contact_id = Column(
        String, source_column="Contact ID 18", contacts_column=P.source_id
    )
    first_name = Column(
        String, source_column="First Name", contacts_column=P.first_name
    )
    last_name = Column(String, source_column="Last Name", contacts_column=P.last_name)
    account_name = Column(String, source_column="Account Name")
    mailing_country = Column(String, source_column="Mailing Country")
    mailing_street = Column(
        String, source_column="Mailing Street", contacts_column=P.street_and_number
    )
    mailing_city = Column(String, source_column="Mailing City", contacts_column=P.city)
    mailing_state_province = Column(
        String, source_column="Mailing State/Province", contacts_column=P.state
    )
    mailing_zip_postal_code = Column(
        String, source_column="Mailing Zip/Postal Code", contacts_column=P.zip
    )
    phone = Column(String, source_column="Phone")
    mobile = Column(String, source_column="Mobile")
    email = Column(String, source_column="Email", contacts_column=P.email)
    json = Column(JSONB)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)

    @classmethod
    def insert_from_file_df(cls, df, conn):
        column_translation = get_source_column_translation(cls)
        df = df[column_translation.keys()]
        df = df.rename(columns=column_translation)

        df["phone"] = df["phone"].apply(normalize_phone_number)
        df["mobile"] = df["mobile"].apply(normalize_phone_number)

        dedup_on = [col for col in cls.__table__.columns if col.name in df.columns]
        df["created_date"] = datetime.datetime.utcnow()
        df.to_sql(cls.__tablename__, conn, if_exists="append", index=False)
        conn.execute(
            dedup_consecutive(
                cls.__table__,
                unique_id=cls._id,
                id=cls.contact_id,
                order_by=cls.created_date,
                dedup_on=tuple_(*dedup_on),
            )
        )

    @classmethod
    def insert_into_pdp_contacts(cls):
        column_mapping = get_contacts_mapping(cls) + [
            # Note: current version of SQLalchemy doesn't like seeing the same
            # column object twice in insert().from_select, hence this
            # literal_column. I think this is fixed in a later version?
            (P.apartment, literal_column("mailing_street")),
            (P.mobile, coalesce(cls.mobile, cls.phone)),
            (P.is_organization, cls.account_name.not_like("% Household")),
        ]
        contacts_columns, this_columns = zip(*column_mapping)

        return insert(PdpContacts).from_select(
            list(contacts_columns),
            select(*this_columns)
            .distinct(cls.contact_id)
            .order_by(cls.contact_id, desc(cls.created_date)),
        )


class ShelterluvPeople(Base):
    __tablename__ = "shelterluvpeople"

    _id = Column(Integer, primary_key=True)
    firstname = Column(String, source_column="Firstname", contacts_column=P.first_name)
    lastname = Column(String, source_column="Lastname", contacts_column=P.last_name)
    id = Column(String, source_column="ID")
    internal_id = Column(
        String, source_column="Internal-ID", contacts_column=P.source_id
    )
    associated = Column(String, source_column="Associated")
    street = Column(String, source_column="Street", contacts_column=P.street_and_number)
    apartment = Column(String, source_column="Apartment", contacts_column=P.apartment)
    city = Column(String, source_column="City", contacts_column=P.city)
    state = Column(String, source_column="State", contacts_column=P.state)
    zip = Column(String, source_column="Zip", contacts_column=P.zip)
    email = Column(String, source_column="Email", contacts_column=P.email)
    phone = Column(String, source_column="Phone", contacts_column=P.mobile)
    animal_ids = Column(JSONB, source_column="Animal_ids")
    json = Column(JSONB)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)

    @classmethod
    def insert_from_df(cls, df, conn):
        column_translation = get_source_column_translation(cls)
        df = df[column_translation.keys()]
        df = df.rename(columns=column_translation)

        df["phone"] = df["phone"].apply(normalize_phone_number)

        dedup_on = [col for col in cls.__table__.columns if col.name in df.columns]
        df["created_date"] = datetime.datetime.utcnow()
        df.to_sql(
            cls.__tablename__,
            conn,
            dtype={"animal_ids": JSONB},
            if_exists="append",
            index=False,
        )
        conn.execute(
            dedup_consecutive(
                cls.__table__,
                unique_id=cls._id,
                id=cls.internal_id,
                order_by=cls.created_date,
                dedup_on=tuple_(*dedup_on),
            )
        )

    @classmethod
    def insert_into_pdp_contacts(cls):
        column_mapping = get_contacts_mapping(cls)
        contacts_columns, this_columns = zip(*column_mapping)
        return insert(PdpContacts).from_select(
            list(contacts_columns),
            select(*this_columns)
            .distinct(cls.internal_id)
            .order_by(cls.internal_id, desc(cls.created_date)),
        )


class Volgistics(Base):
    __tablename__ = "volgistics"

    _id = Column(Integer, primary_key=True)
    number = Column(String, source_column="Number", contacts_column=P.source_id)
    last_name = Column(String, source_column="Last name", contacts_column=P.last_name)
    first_name = Column(
        String, source_column="First name", contacts_column=P.first_name
    )
    middle_name = Column(String, source_column="Middle name")
    complete_address = Column(String, source_column="Complete address")
    street_1 = Column(String, source_column="Street 1")
    street_2 = Column(String, source_column="Street 2")
    street_3 = Column(String, source_column="Street 3")
    city = Column(String, source_column="City", contacts_column=P.city)
    state = Column(String, source_column="State", contacts_column=P.state)
    zip = Column(String, source_column="Zip", contacts_column=P.zip)
    all_phone_numbers = Column(String, source_column="All phone numbers")
    home = Column(String, source_column="Home")
    work = Column(String, source_column="Work")
    cell = Column(String, source_column="Cell")
    email = Column(String, source_column="Email", contacts_column=P.email)
    json = Column(JSONB)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)

    @classmethod
    def insert_from_file(cls, xl_file, conn):
        df = pd.read_excel(xl_file, sheet_name="Master")

        column_translation = get_source_column_translation(cls)
        df = df[column_translation.keys()]
        df = df.rename(columns=column_translation)

        df["home"] = df["home"].apply(normalize_phone_number)
        df["work"] = df["work"].apply(normalize_phone_number)
        df["cell"] = df["home"].apply(normalize_phone_number)

        dedup_on = [col for col in cls.__table__.columns if col.name in df.columns]
        df["created_date"] = datetime.datetime.utcnow()
        df.to_sql(
            cls.__tablename__,
            conn,
            if_exists="append",
            index=False,
        )
        conn.execute(
            dedup_consecutive(
                cls.__table__,
                unique_id=cls._id,
                id=cls.number,
                order_by=cls.created_date,
                dedup_on=tuple_(*dedup_on),
            )
        )

    @classmethod
    def insert_into_pdp_contacts(cls):
        column_mapping = get_contacts_mapping(cls) + [
            # NOTE: This logic seems wrong. It peels off the streat number and
            # calls it the "apartment," and calls the rest of the address the
            # "street and number."
            (
                P.street_and_number,
                literal_column("regexp_replace(street_1, '^[^ ]* ?', '')"),
            ),
            (P.apartment, literal_column("(regexp_match(street_1, '^([^ ]*) '))[1]")),
            (P.mobile, coalesce(cls.cell, cls.home)),
        ]
        contacts_columns, this_columns = zip(*column_mapping)
        return insert(PdpContacts).from_select(
            list(contacts_columns),
            select(*this_columns)
            .distinct(cls.number)
            .order_by(cls.number, desc(cls.created_date)),
        )


class ManualMatches(Base):
    __tablename__ = "manual_matches"

    source_type_1 = Column(String, primary_key=True)
    source_id_1 = Column(String, primary_key=True)
    source_type_2 = Column(String, primary_key=True)
    source_id_2 = Column(String, primary_key=True)

    @classmethod
    def insert_from_df(cls, df, conn):
        # Our input csv has columns like "salesforcecontacts," "volgistics," and
        # "shelterluvpeople," where two columns are non-null if there is an
        # association between those two ids. We massage this table into one that
        # is easier to join on.
        
        match_dicts = df.to_dict(orient="records")

        matched_pairs = []
        for match in match_dicts:
            non_nulls = {k: v for (k, v) in match.items() if not pd.isna(v)}
            for ((st1, sid1), (st2, sid2)) in combinations(non_nulls.items(), 2):
                matched_pairs.append(
                    {
                        "source_type_1": st1,
                        "source_id_1": sid1,
                        "source_type_2": st2,
                        "source_id_2": sid2,
                    }
                )

        conn.execute(insert(cls).values(matched_pairs).on_conflict_do_nothing())
