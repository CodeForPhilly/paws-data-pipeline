from config import engine
from api import user_api
import sqlalchemy as sa
import os

import structlog
logger = structlog.get_logger()


try:   
    from secrets_dict import BASEUSER_PW, BASEADMIN_PW
except ImportError:   
    # Not running locally
    logger.debug("Couldn't get BASE user PWs from file, trying environment **********")
    from os import environ

    try:
        BASEUSER_PW = environ['BASEUSER_PW']
        BASEADMIN_PW = environ['BASEADMIN_PW']

    except KeyError:
        # Nor in environment
        # You're SOL for now
        logger.error("Couldn't get secrets from file or environment")





from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

metadata = sa.MetaData()


def create_base_roles():
    with engine.connect() as connection:
        result = connection.execute("select role from pdp_user_roles")
        role_count = len(result.fetchall())
        if role_count == 0:
            connection.execute("INSERT into pdp_user_roles  values (1, 'user') ")
            connection.execute("INSERT into pdp_user_roles  values (9, 'admin') ")

        else:
            logger.debug("%d roles already present in DB, not creating", role_count)


def create_base_users():  # TODO: Just call create_user for each
    """ Creates two users (user, admin) for testing
        Password for each is user name with 'pw' appended """
    with engine.connect() as connection:

        result = connection.execute("select user from pdp_users")
        user_count = len(result.fetchall())
        if user_count == 0:

            logger.debug("Creating base users")

            pu = sa.Table("pdp_users", metadata, autoload=True, autoload_with=engine)

            # user
            pw_hash = user_api.hash_password(BASEUSER_PW)
            ins_stmt = pu.insert().values(
                username="base_user", full_name="Base User", password=pw_hash, active="Y", role=1,
            )
            connection.execute(ins_stmt)

            # INactive user
            # Reuse pw hash
            ins_stmt = pu.insert().values(
                username="base_user_inact", full_name="Inactive User", password=pw_hash, active="N", role=1,
            )
            connection.execute(ins_stmt)

            # admin
            pw_hash = user_api.hash_password(BASEADMIN_PW)
            ins_stmt = pu.insert().values(
                username="base_admin", full_name="Base Admin", password=pw_hash, active="Y", role=9,
            )
            connection.execute(ins_stmt)

        else:
            logger.debug("%d users already present in DB, not creating", user_count)


def populate_sl_event_types():
    """If not present, insert values for shelterluv animal event types."""
    with engine.connect() as connection:
        result = connection.execute("select id from sl_event_types")
        type_count = len(result.fetchall())
        if type_count == 0:
            print("Inserting SL event types")
            connection.execute("""INSERT into sl_event_types values 
                                (1, 'Outcome.Adoption'),
                                (2, 'Outcome.Foster'),
                                (3, 'Outcome.ReturnToOwner'),
                                (4, 'Intake.AdoptionReturn'),
                                (5, 'Intake.FosterReturn'); """)                                     
        else:
            logger.debug("%d event types already present in DB, not creating", type_count)
