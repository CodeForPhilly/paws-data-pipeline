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
    hash = pbkdf2_hmac("sha512", bytes(password, "utf8"), salt, 500000)
    hash_for_db = salt + hash
    return hash_for_db


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
    """Liveness test"""
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
    username = request.form["username"]

    # For now, just echo the data
    log_user_action("Logged out " + username)
    return jsonify("Logged out " + username)


@user_api.route("/user/create", methods=["POST"])
@jwt_ops.admin_required
def user_create():
    """Create user record 
    
    Requires admin role  

    Form POST Parameters  
    ----------
    username : str  
    full_name : str  
    password : str  
    role : str, one of `user`, `editor`, `admin`  

    Returns    
    ----------
    User created: 201 + username  
    Invalid role: 422 + "Bad role"  
    Duplicate user: 409 +  DB error  

    """
    new_user = request.form["username"]
    fullname = request.form["full_name"]
    userpw = request.form["password"]
    user_role = request.form["role"]

    pw_hash = hash_password(userpw)

    pu = Table("pdp_users", metadata, autoload=True, autoload_with=engine)
    pr = Table("pdp_user_roles", metadata, autoload=True, autoload_with=engine)

    with engine.connect() as connection:

        # Build dict of roles
        role_dict = {}
        r = select((pr.c.role, pr.c._id))
        rr = connection.execute(r)
        fa = rr.fetchall()
        for row in fa:
            role_dict[row[0]] = row[1]  # TODO: possible to do directly in sa?

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


@user_api.route("/user/deactivate", methods=["POST"])
@jwt_ops.admin_required
def user_deactivate():
    """Mark user as inactive in DB"""

    return "", 200


@user_api.route("/user/activate", methods=["POST"])
@jwt_ops.admin_required
def user_activate():
    """Mark user as active in DB"""

    return "", 200


@user_api.route("/user/get_users", methods=["GET"])
@jwt_ops.admin_required
def user_get_list():
    """Return list of users"""

    # pu = Table("pdp_users", metadata, autoload=True, autoload_with=engine)
    #  pr = Table("pdp_user_roles", metadata, autoload=True, autoload_with=engine)

    with engine.connect() as connection:

        s = text(
            """ select username, full_name, active, pr.role
            from pdp_users as pu 
            left join pdp_user_roles as pr on pu.role = pr._id
            order by username """
        )
        result = connection.execute(s)

        user_list = ""

        for row in result:
            user_list += str(row.values()) + ","

        ul = str(row.keys()) + "," + user_list

    return jsonify(ul), 200


# Keep a journal of user activity
def log_user_action(action):

    # for now, just print to stdout
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
