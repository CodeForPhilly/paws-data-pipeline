from config import db
from api import user_api
import sqlalchemy as sa
import os



try:   
    from secrets_dict import BASEUSER_PW, BASEEDITOR_PW, BASEADMIN_PW
except ImportError:   
    # Not running locally
    print("Couldn't get BASE user PWs from file, trying environment **********")
    from os import environ

    try:
        BASEUSER_PW = environ['BASEUSER_PW']
        BASEEDITOR_PW = environ['BASEEDITOR_PW']
        BASEADMIN_PW = environ['BASEADMIN_PW']

    except KeyError:
        # Nor in environment
        # You're SOL for now
        print("Couldn't get secrets from file or environment")





from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

metadata = sa.MetaData()


def create_base_roles():
    with db.engine.connect() as connection:
        result = connection.execute("select role from pdp_user_roles")
        role_count = len(result.fetchall())
        if role_count == 0:
            connection.execute("INSERT into pdp_user_roles  values (1, 'user') ")
            connection.execute("INSERT into pdp_user_roles  values (2, 'editor') ")
            connection.execute("INSERT into pdp_user_roles  values (9, 'admin') ")

        else:
            print(role_count, "roles already present in DB, not creating")


def create_base_users():  # TODO: Just call create_user for each
    """ Creates three users (user, editor, admin) for testing
        Password for each is user name with 'pw' appended """
    with db.engine.connect() as connection:

        result = connection.execute("select user from pdp_users")
        user_count = len(result.fetchall())
        if user_count == 0:

            print("Creating base users")

            pu = sa.Table("pdp_users", metadata, autoload=True, autoload_with=db.engine)

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

            # editor
            pw_hash = user_api.hash_password(BASEEDITOR_PW)
            ins_stmt = pu.insert().values(
                username="base_editor", full_name="Base Editor", password=pw_hash, active="Y", role=2,
            )
            connection.execute(ins_stmt)

            # admin
            pw_hash = user_api.hash_password(BASEADMIN_PW)
            ins_stmt = pu.insert().values(
                username="base_admin", full_name="Base Admin", password=pw_hash, active="Y", role=9,
            )
            connection.execute(ins_stmt)

        else:
            print(user_count, "users already present in DB, not creating")


def populate_rfm_mapping_table(overwrite=False):
    """Populate the rfm_mapping table if empty or overwrite is True."""

    with db.engine.connect() as connection:

        def table_empty():
            result = connection.execute("select count(*) from rfm_mapping;")
            row_count = result.fetchone()[0]
            return row_count == 0


        if overwrite or table_empty():
            print("Populating rfm_mapping table")

            if not table_empty():
                print("'overwrite=True', truncating rfm_mapping table")
                connection.execute("TRUNCATE TABLE rfm_mapping;")


            if os.path.exists('server'):    # running locally
                file_path = os.path.normpath('server/alembic/populate_rfm_mapping.sql')

            elif os.path.exists('alembic'):  # running on Docker
                file_path = os.path.normpath('alembic/populate_rfm_mapping.sql')

            else:                 #
                print("ERROR: Can't find a path to populate script!!!!!!")
                print('CWD is ' + os.getcwd())
                return



            print("Loading sql script at " + file_path)

            f = open(file_path)
            populate_query = f.read()
            f.close()

            result = connection.execute(populate_query)

            if table_empty():
                print("ERROR:        rfm_mapping table WAS NOT POPULATED")

        else:
            print("rfm_mapping table already populated; overwrite not True so not changing.")

    return