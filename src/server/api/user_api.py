from hashlib import pbkdf2_hmac
from os import urandom
import pytest, codecs

from api.api import user_api
from sqlalchemy.sql import text
from config import engine
from flask import request, redirect, jsonify, current_app, abort

# from profile import init_db_schema
import jwt_ops

#
import random

# jwt_ops.JWT_init()

# init_db_schema.start()

SALT_LENGTH = 32

# Generate salt+hash for storing in db
def hash_password(password):
    salt = urandom(SALT_LENGTH)
    print("Salt:", salt, len(salt))
    hash = pbkdf2_hmac("sha512", password, salt, 500000)
    print("Hash:", hash, len(hash))
    hash_for_db = salt + hash
    print("Hash for db", hash_for_db)
    return hash_for_db


# Check presented password against what's in the db
def check_password(password, salty_hash):
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
    # Lookup user in db

    with engine.connect() as connection:

        pwhash = None
        s = text("select password, role from pdp_users where username=:u")
        s = s.bindparams(u=request.form["username"])
        result = connection.execute(s)
        pwhash, role = result.fetchone()

        if check_password(request.form["password"], pwhash):
            return jwt_ops.create_token(request.form["username"], role)
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


# Create new user
@user_api.route("/user/create", methods=["POST"])
# Requestor must have admin role, else 403
def user_create():

    new_user = request.form["username"]
    user_role = request.form["role"]

    user_id = random.randrange(1, 200)

    # User must not already exist, else 409 ?

    # if created, 201
    log_user_action(
        "DUMMY LOG: Created account for "
        + new_user
        + " as id "
        + str(user_id)
        + " with role "
        + user_role
    )
    return jsonify(user_id), 201


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
