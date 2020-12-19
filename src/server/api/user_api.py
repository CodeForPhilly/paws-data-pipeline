from hashlib import pbkdf2_hmac
from os import urandom
import pytest, codecs, random

from api.api import user_api
from sqlalchemy.sql import text
from config import engine
from flask import request, redirect, jsonify, current_app, abort

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, exc, select

import jwt_ops


metadata = MetaData()

# Salt for hashing storing passwords
SALT_LENGTH = 32


def hash_password(password):
    """ Generate salt+hash for storing in db"""
    salt = urandom(SALT_LENGTH)
    print("Salt:", salt, len(salt))
    hash = pbkdf2_hmac("sha512", bytes(password, "utf8"), salt, 500000)
    print("Hash:", hash, len(hash))
    hash_for_db = salt + hash
    print("Hash for db", hash_for_db)
    return hash_for_db


# Check presented password against what's in the db
def check_password(password, salty_hash):
    """Check presented cleartext password aginst DB-type salt+hash, return True if they match"""
    salt = salty_hash[0:SALT_LENGTH]
    hash = salty_hash[SALT_LENGTH:]
    # Use salt from db to hash what user gave us
    pw_bytes = bytes(password, "utf8")
    hash_of_presented = pbkdf2_hmac("sha512", pw_bytes, salt, 500000)
    return hash.hex() == hash_of_presented.hex()


@user_api.route("/user/test", methods=["GET"])
def user_test():
    return jsonify("OK from User Test")


# Verify username and password, return a JWT with role
@user_api.route("/user/login", methods=["POST"])
def user_login():
    """ Validate user in db, return JWT if legit"""

    with engine.connect() as connection:

        pwhash = None
        s = text(
            """select password, pdp_user_roles.role 
                from pdp_users 
                left join pdp_user_roles on pdp_users.role = pdp_user_roles._id 
                where username=:u """
        )
        s = s.bindparams(u=request.form["username"])
        result = connection.execute(s)

        if result.rowcount:  # Did we get a match on username?
            pwhash, role = result.fetchone()
        else:
            return jsonify("Bad credentials"), 401

        if check_password(request.form["password"], pwhash):
            # Yes, user is valid & password matches
            token = jwt_ops.create_token(request.form["username"], role)
            return token

        else:
            return jsonify("Bad credentials"), 401


# Logout is not strictly neeed; client can just delete JWT, but good for logging
@user_api.route("/user/logout", methods=["POST"])
def user_logout():
    # Lookup user in db
    user_id = request.form["user_id"]

    # For now, just echo the data
    log_user_action("Logged out " + str(user_id))
    return jsonify("Logged out " + str(user_id))


# TODO: Re-enable admin check
@user_api.route("/user/create", methods=["POST"])
@jwt_ops.admin_required
def user_create():
    """Create user record from username, full_name, password, role """
    new_user = request.form["username"]
    fullname = request.form["full_name"]
    userpw = request.form["password"]
    user_role = request.form["role"]

    pw_hash = hash_password(userpw)

    pu = Table("pdp_users", metadata, autoload=True, autoload_with=engine)
    pr = Table("pdp_user_roles", metadata, autoload=True, autoload_with=engine)

    # TODO: Get list of roles, use value

    with engine.connect() as connection:

        # Build dict of roles
        role_dict = {}
        r = select((pr.c.role, pr.c._id))
        rr = connection.execute(r)
        fa = rr.fetchall()
        for row in fa:
            role_dict[row[0]] = row[1]

        try:
            role_val = role_dict[user_role]
        except KeyError as e:
            print("Role not found", e)
            return jsonify("Bad role"), 422

        ins_stmt = pu.insert().values(
            # _id=default,
            username=new_user,
            password=pw_hash,
            full_name=fullname,
            active="Y",
            role=role_val,
        )

        try:
            connection.execute(ins_stmt)
        except exc.IntegrityError as e:  # Uniqueness violation
            return jsonify(e.orig.pgerror), 409

    # if created, 201
    log_user_action(
        "DUMMY LOG: Created account for "
        + new_user
        + " ( "
        + fullname
        + " ) "
        + " with role "
        + user_role
    )
    return jsonify(new_user), 201


def get_user_count():
    """Return number of records in pdp_users table """
    with engine.connect() as connection:
        s = text("select count(user) from pdp_users;")
        result = connection.execute(s)
        user_count = result.fetchone()
        return user_count[0]


# Keep a journal of user activity
def log_user_action(action):

    # for now, just print to stdin
    print(action)


def test_pw_hashing():
    test_pw = codecs.encode("long complicated password ##$& λογοσ δοζα", "utf8")

    print("Test pw:", test_pw)

    db_hash = hash_password(test_pw)
    print("DB hash", db_hash)

    good = check_password(test_pw, db_hash)
    bad = check_password(test_pw + b"xxx", db_hash)
    print("Good, bad:", good, bad)
    return good and not bad
