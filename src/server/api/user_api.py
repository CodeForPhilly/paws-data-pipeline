from hashlib import pbkdf2_hmac
from os import urandom
import pytest, codecs, random
from datetime import datetime

from api.api import user_api
from sqlalchemy.sql import text
from config import engine
from flask import request, redirect, jsonify, current_app, abort, json

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, exc, select

from api import jwt_ops


metadata = MetaData()

# Salt for hashing storing passwords
SALT_LENGTH = 32


# Keep a journal of user activity
def log_user_action(user, event_class, detail):
    """ Write log entry to db """

    puj = Table("pdp_user_journal", metadata, autoload=True, autoload_with=engine)

    with engine.connect() as connection:
        ins_stmt = puj.insert().values(username=user, event_type=event_class, detail=detail)

        try:
            connection.execute(ins_stmt)
        except Exception as e:
            print(e)


def hash_password(password):
    """ Generate salt+hash for storing in db"""
    salt = urandom(SALT_LENGTH)
    hash = pbkdf2_hmac("sha512", bytes(password, "utf8"), salt, 500000)
    hash_for_db = salt + hash
    return hash_for_db


def check_password(password, salty_hash):
    """Check presented cleartext password against DB-type salt+hash, return True if they match"""
    salt = salty_hash[0:SALT_LENGTH]
    hash = salty_hash[SALT_LENGTH:]
    # Use salt from db to hash what user gave us
    pw_bytes = bytes(password, "utf8")
    hash_of_presented = pbkdf2_hmac("sha512", pw_bytes, salt, 500000)
    return hash.hex() == hash_of_presented.hex()


###     No authorization required              ############################


@user_api.route("/api/user/test", methods=["GET"])
def user_test():
    """ Liveness test, does not require JWT """
    return jsonify(("OK from User Test  @ " + str(datetime.now())))


@user_api.route("/api/user/test_fail", methods=["GET"])
def user_test_fail():
    """ Liveness test, always fails with 401"""
    return jsonify("Here's your failure"), 401



@user_api.route("/api/user/login_json", methods=["POST"])
def user_login_json():
    """ Validate user in db, return JWT if legit and active.
        Expects json-encoded form data
    """

    def dummy_check():
        """Perform a fake password hash check to take as much time as a real one."""
        pw_bytes = bytes('password', "utf8")
        check_password('password', pw_bytes)

    try:
        post_dict = json.loads(request.data)
        username = post_dict["username"]
        presentedpw = post_dict["password"]
    except:
        dummy_check()    # Take the same time as with well-formed requests 
        return jsonify("Bad credentials"), 401

    if not (isinstance(username, str) and isinstance(presentedpw, str) ):
        dummy_check()  # Take the same time as with well-formed requests 
        return jsonify("Bad credentials"), 401   # Don't give us ints, arrays, etc.


    with engine.connect() as connection:

        pwhash = None
        s = text(
            """select password, pdp_user_roles.role, active 
                from pdp_users 
                left join pdp_user_roles on pdp_users.role = pdp_user_roles._id 
                where username=:u """
        )
        s = s.bindparams(u=username)
        result = connection.execute(s)

        if result.rowcount:  # Did we get a match on username?
            pwhash, role, is_active = result.fetchone()
        else:
            log_user_action(username, "Failure", "Invalid username")
            dummy_check()
            return jsonify("Bad credentials"), 401

        if is_active.lower() == "y" and check_password(presentedpw, pwhash):
            # Yes, user is active and password matches
            token = jwt_ops.create_token(username, role)
            log_user_action(username, "Success", "Logged in")
            return token

        else:
            log_user_action(username, "Failure", "Bad password or inactive")
            # No dummy_check needed as we ran a real one to get here
            return jsonify("Bad credentials"), 401


###    Unexpired JWT required               ############################


@user_api.route("/api/user/test_auth", methods=["GET"])
@jwt_ops.jwt_required()
def user_test_auth():
    """ Liveness test, requires JWT """
    return jsonify(("OK from User Test - Auth  @" + str(datetime.now())))


# Logout is not strictly needed; client can just delete JWT, but good for logging
@user_api.route("/api/user/logout", methods=["POST"])
@jwt_ops.jwt_required()
def user_logout():
    username = request.form["username"]  # TODO: Should be JSON all throughout
    # Log the request
    log_user_action(username, "Success", "Logged out ")
    return jsonify("Logged out " + username)


###    Unexpired *Admin* JWT  required      ############################


@user_api.route("/api/admin/user/create", methods=["POST"])
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

    requesting_user = jwt_ops.get_jwt_user()

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
            log_user_action(
                requesting_user,
                "Failure",
                "Bad role (" + user_role + ") in user_create for " + new_user,
            )
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
        requesting_user, "Success", "Created user " + new_user + " with role: " + user_role,
    )
    return jsonify(new_user), 201


@user_api.route("/api/admin/user/get_user_count", methods=["GET"])
@jwt_ops.admin_required
def get_user_count():
    """Return number of records in pdp_users table """
    with engine.connect() as connection:
        s = text("select count(user) from pdp_users;")
        result = connection.execute(s)
        user_count = result.fetchone()
        return jsonify(user_count[0])


# TODO: A single do-all update_user()
@user_api.route("/api/admin/user/deactivate", methods=["POST"])
@jwt_ops.admin_required
def user_deactivate():
    """Mark user as inactive in DB"""
    # TODO
    return "", 200


@user_api.route("/api/admin/user/activate", methods=["POST"])
@jwt_ops.admin_required
def user_activate():
    """Mark user as active in DB"""
    # TODO
    return "", 200


@user_api.route("/api/admin/user/get_users", methods=["GET"])
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

