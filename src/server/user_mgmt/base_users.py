from sqlalchemy.sql.schema import ColumnDefault
from config import engine
from api import user_api
import sqlalchemy as sa

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

metadata = sa.MetaData()


def create_base_roles():
    with engine.connect() as connection:
        result = connection.execute("select role from pdp_user_roles")
        role_count = len(result.fetchall())
        if role_count == 0:
            connection.execute("INSERT into pdp_user_roles  values (0, 'user') ")
            connection.execute("INSERT into pdp_user_roles  values (1, 'editor') ")
            connection.execute("INSERT into pdp_user_roles  values (9, 'admin') ")

        else:
            print(role_count, "roles already present in DB, not creating")


def create_base_users():
    with engine.connect() as connection:

        # ins = pdp_users.insert()

        result = connection.execute("select user from pdp_users")
        user_count = len(result.fetchall())
        if user_count == 0:

            pu = sa.Table("pdp_users", metadata, autoload=True, autoload_with=engine)
            pw_hash = user_api.hash_password(b"userpw")

            ins_stmt = pu.insert().values(
                # _id=default,
                username="user",
                password=pw_hash,
                # created=sa.ColumnDefault,
                active="Y",
                role=1,
            )

            connection.execute(ins_stmt)

            pw_hash = user_api.hash_password(b"editorpw")

            ins_stmt = pu.insert().values(
                username="editor", password=pw_hash, active="Y", role=2,
            )

            connection.execute(ins_stmt)

            pw_hash = user_api.hash_password(b"adminpw")

            ins_stmt = pu.insert().values(
                username="admin", password=pw_hash, active="Y", role=9,
            )

            connection.execute(ins_stmt)

        # connection.execute(
        #     "INSERT into pdp_users  values (Default, 'editor','editorpw',  'Y', Default,  2) "
        # )
        # connection.execute(
        #     "INSERT into pdp_users  values (Default, 'admin', 'adminpw',  'Y', Default,  9) "
        # )

        else:
            print(user_count, "users already present in DB, not creating")
