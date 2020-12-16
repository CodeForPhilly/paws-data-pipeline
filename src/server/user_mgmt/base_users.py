from config import engine
from flask import request, redirect, jsonify, current_app, abort
import datetime


def create_base_roles(connection):
    with engine.connect() as connection:
        result = connection.execute("select role from pdp_user_roles")
        if len(result.fetchall()) == 0:
            connection.execute("INSERT into pdp_user_roles  values (0, 'user') ")
            connection.execute("INSERT into pdp_user_roles  values (1, 'editor') ")
            connection.execute("INSERT into pdp_user_roles  values (9, 'admin') ")


def create_base_users(connection):
    with engine.connect() as connection:
        result = connection.execute("select user from pdp_users")
        if len(result.fetchall()) == 0:
            connection.execute(
                "INSERT into pdp_users  values (0, 'user', Default, 'Y', 'user', 'userpw') "
            )
            connection.execute(
                "INSERT into pdp_users  values (1, 'editor', Default,'Y', 'editor', 'editorpw') "
            )
            connection.execute(
                "INSERT into pdp_users  values (2, 'admin',  datetime.datetime.utcnow(), 'Y', 'admin', 'adminpw') "
            )

