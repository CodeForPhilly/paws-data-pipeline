from sqlalchemy.sql.schema import ColumnDefault
from config import engine
from api import user_api
import sqlalchemy as sa

from secrets import BASEUSER_PW, BASEEDITOR_PW, BASEADMIN_PW


from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

metadata = sa.MetaData()


def create_base_roles():
    with engine.connect() as connection:
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
    with engine.connect() as connection:

        result = connection.execute("select user from pdp_users")
        user_count = len(result.fetchall())
        if user_count == 0:

            print("Creating base users")

            pu = sa.Table("pdp_users", metadata, autoload=True, autoload_with=engine)

            # user
            pw_hash = user_api.hash_password(BASEUSER_PW)
            ins_stmt = pu.insert().values(
                username="base_user", password=pw_hash, active="Y", role=1,
            )
            connection.execute(ins_stmt)

            # INactive user
            # Reuse pw hash
            ins_stmt = pu.insert().values(
                username="base_user_inact", password=pw_hash, active="N", role=1,
            )
            connection.execute(ins_stmt)

            # editor
            pw_hash = user_api.hash_password(BASEEDITOR_PW)
            ins_stmt = pu.insert().values(
                username="base_editor", password=pw_hash, active="Y", role=2,
            )
            connection.execute(ins_stmt)

            # admin
            pw_hash = user_api.hash_password(BASEADMIN_PW)
            ins_stmt = pu.insert().values(
                username="base_admin", password=pw_hash, active="Y", role=9,
            )
            connection.execute(ins_stmt)

        else:
            print(user_count, "users already present in DB, not creating")
