from api.api import user_api
from sqlalchemy.sql import text
from config import engine
from flask import request, redirect, jsonify, current_app, abort

import jwt_ops

#
import random

# jwt_ops.JWT_init()


@user_api.route("/user/test", methods=["GET"])
def user_test():
    return jsonify("OK from User Test")


# Verify username and password, return a JWT with role
@user_api.route("/user/login", methods=["POST"])
def user_login():
    # Lookup user in db

    # For now, just echo the data
    return jwt_ops.create_token(37, "JoeUser", "Admin")


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
