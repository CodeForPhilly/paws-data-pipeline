from hashlib import pbkdf2_hmac
from os import urandom, environ
import pytest, codecs, random
from datetime import datetime

from api.api import user_api
from sqlalchemy.sql import text
from config import engine
from flask import request, redirect, jsonify, current_app, abort, json

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, exc, select

from api import jwt_ops

import structlog
logger = structlog.get_logger()


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
            logger.error(e)

def password_is_strong(password):
    """ Check plain-text password against strength rules."""

    def has_digit(test_string):
        """Test if any character is a digit."""
        for c in test_string:
            if c.isdigit():
                return True
        return False

    def has_alpha(test_string):
        """Test if any character is  alphabetic."""
        for c in test_string:
            if c.isalpha():
                return True
        return False

    if (len(password) > 11   
        # and has_alpha(password) 
        # and has_digit(password)
         ):
        return True
    
    else:
        return False


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
    logger.debug("/api/user/test")
    return jsonify(("OK from User Test  @ " + str(datetime.now())))


@user_api.route("/api/user/test_log", methods=["GET"])
def user_test_log_error():
    """Does not require JWT  - see various log levels"""

    logger.debug("debug: /api/user/test_log_error")        
    logger.info("info: /api/user/test_log_error")    
    logger.warn("warn: /api/user/test_log_error")
    logger.error("error: /api/user/test_log_error")
    logger.critical("critical: /api/user/test_log_error")
    return jsonify(("Generated log entries as various levals  @ " + str(datetime.now())))




@user_api.route("/api/user/test_fail", methods=["GET"])
def user_test_fail():
    """ Liveness test, always fails with 401"""
    return jsonify("Here's your failure"), 401


@user_api.route("/api/user/timeout/<int:new_timeout>", methods=["GET"])
def user_override_timeout(new_timeout):
    """ Override JWT expiration setting for testing.
        Allows a value up to JWT_MAX_TIMEOUT (from app.py).
        This will affect, of course, only future tokens.
    """  
    if (new_timeout > current_app.config["JWT_MAX_TIMEOUT"] ) : 
        new_timeout = current_app.config["JWT_MAX_TIMEOUT"]
    current_app.config["JWT_ACCESS_TOKEN_EXPIRES"] = new_timeout
    return jsonify("Timeout set to " + str(new_timeout) + " seconds"), 200


@user_api.route("/api/user/login", methods=["POST"])
def user_login():
    """ Validate user in db, return JWT if legit and active.
        Expects json-encoded form data {"username" :, "password": }
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
    sysname = '?'    # Ensure we are talking to the expected host
    try:
        sysname = environ['computername'] 
    except:
        pass
    
    try:
        sysname =  environ['HOSTNAME']
    except:
        pass


    return jsonify(("OK from User Test - Auth [" + sysname + "] @" + str(datetime.now())))


# Logout is not strictly needed; client can just delete JWT, but good for logging
@user_api.route("/api/user/logout", methods=["POST"])
@jwt_ops.jwt_required()
def user_logout():
    
    user_name = ''

    old_jwt = jwt_ops.validate_decode_jwt()   

    # If token bad, should be handled & error message sent by jwt_required() and we won't get here
    if old_jwt:
        user_name = old_jwt['sub']
    
    # Log the request
    log_user_action(user_name, "Success", "Logged out")
    return jsonify("Logged out")


# Generate a new access token 

@user_api.route("/api/user/refresh", methods=["GET"])
@jwt_ops.jwt_required()
def user_refresh():
    """ If user still active, send back an access_token with a new expiration stamp """
    old_jwt = jwt_ops.validate_decode_jwt()   

    # If token bad, should be handled & error message sent by jwt_required() and we won't get here
    if old_jwt:
        user_name = old_jwt['sub']
        with engine.connect() as connection:

            s = text( """select active from pdp_users where username=:u """ )
            s = s.bindparams(u=user_name)
            result = connection.execute(s)

            if result.rowcount:  # Did we get a match on username?
                is_active = result.fetchone()
            else:
                log_user_action(user_name, "Failure", "Valid JWT presented for refesh attempt on unknown username")
                return jsonify("Bad credentials"), 401

            if is_active[0].lower() == 'y':    # In the user DB and still Active?
                token = jwt_ops.create_token(user_name,old_jwt['role'])
                log_user_action(user_name, "Success", "Refreshed token")
                return token

    else:
        return jsonify("Bad credentials"), 401



###    Unexpired *Admin* JWT  required      ############################


@user_api.route("/api/admin/user/create", methods=["POST"])
@jwt_ops.admin_required
def user_create():
    """Create user record 
    
    Requires admin role  

    Form POST JSON Parameters  
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

    try:
        post_dict = json.loads(request.data)
        new_user = post_dict["username"]
        fullname = post_dict["full_name"]
        userpw = post_dict["password"]
        user_role = post_dict["role"]
    except:
        return jsonify("Missing one or more parameters"), 400


    requesting_user = jwt_ops.validate_decode_jwt()['sub'] 

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
            logger.error("Role not found %s", e)
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


@user_api.route("/api/admin/user/check_name", methods=["POST"])
@jwt_ops.admin_required
def check_username():
    """Return 1 if username exists already, else 0."""

    try:
        post_dict = json.loads(request.data)
        test_username = post_dict["username"]
    except:
        return jsonify("Missing username"), 400

    with engine.connect() as connection:

        s = text( """select count(username)  from pdp_users where username=:u """ )
        s = s.bindparams(u=test_username)
        result = connection.execute(s)

        if result.rowcount:  # As we're doing a count() we *should* get a result
            user_exists = result.fetchone()[0]
        else:
            log_user_action(test_username, "Failure", "Error when checking username")
            return jsonify("Error checking username"), 500

        return jsonify(user_exists)

@user_api.route("/api/admin/user/update", methods=["POST"])
@jwt_ops.admin_required  
def user_update():
    """Update existing user record 
    """
  
   
    try:
        post_dict = json.loads(request.data)
        username = post_dict["username"]
    except:
        return jsonify("Must specify username"), 400

    update_dict = {}

    # Need to be a bit defensive here & select what we want instead of taking what we're given
    for key in ["full_name", "active", "role", "password"]: 
        try:
            val = post_dict[key]
            update_dict[key] = val
        except:
            pass

    
    if not update_dict:
        return jsonify("No changed items specified")  # If nothing to do, declare victory

    if "password" in update_dict.keys():

        if password_is_strong(update_dict['password']):
            update_dict['password'] = hash_password(update_dict['password'])
        else:
            return jsonify("Password too weak") 



    #  We have a variable number of columns to update.
    #  We could generate a text query on the fly, but this seems the perfect place to use the ORM  
    #  and let it handle the update for us. 

    from sqlalchemy import update
    from sqlalchemy.orm import Session, sessionmaker

    Session = sessionmaker(engine)

    session =  Session()   
   # #TODO: Figure out why context manager doesn't work or do try/finally

    PU = Table("pdp_users", metadata, autoload=True, autoload_with=engine)
    #  pr = Table("pdp_user_roles", metadata, autoload=True, autoload_with=engine)

    #TODO: Check tendered role or join roles table for update

    stmt = update(PU).where(PU.columns.username == username).values(update_dict).\
        execution_options(synchronize_session="fetch")

    result = session.execute(stmt)

    session.commit()
    session.close()

    return jsonify("Updated")


@user_api.route("/api/admin/user/get_users", methods=["GET"])
@jwt_ops.admin_required
def user_get_list():
    """Return list of users"""

    with engine.connect() as connection:

        s = text(
            """ select username, full_name, active, pr.role
            from pdp_users as pu 
            left join pdp_user_roles as pr on pu.role = pr._id
            order by username """
        )
        result = connection.execute(s)

        query_result_json = [dict(row) for row in result]

    return jsonify(query_result_json), 200

@user_api.route("/api/admin/user/get_info/<string:username>", methods=["GET"])
@jwt_ops.admin_required  
def user_get_info(username):
    """Return info on a specified user"""

    with engine.connect() as connection:

        s = text(
            """ select username, full_name, active, pr.role
            from pdp_users as pu 
            left join pdp_user_roles as pr on pu.role = pr._id
            where username=:u
            """
        )
        s = s.bindparams(u=username)
        result = connection.execute(s)
        
        if result.rowcount:  
            user_row = result.fetchone()
        else:
            log_user_action(username, "Failure", "Error when getting user info")
            return jsonify("Username not found"), 400

    return jsonify( dict(zip(result.keys(), user_row)) ), 200