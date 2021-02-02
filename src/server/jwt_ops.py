from functools import wraps
from flask import Flask, jsonify, request, current_app
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    get_jwt_identity,
    verify_jwt_in_request,
    get_jwt_claims,
)

from app import app, jwt

# Wraps funcs to require admin role to execute
def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims["role"] != "admin":  # TODO could be multiple
            return jsonify(msg="Admins only!"), 403
        else:
            return fn(*args, **kwargs)

    return wrapper


# Provide a method to create access tokens. The create_access_token()
# function is used to actually generate the token, and you can return
# it to the caller however you choose.
@app.route("/login", methods=["POST"])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    if username == "admin" and password == "admin":
        accesslevel = "admin"
    elif username == "test" and password == "test":
        accesslevel = "user"
    else:
        return jsonify({"msg": "Bad username or password"}), 401

    @jwt.user_claims_loader
    def add_claims_to_access_token(identity):
        return {"role": accesslevel}

    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200


@jwt.user_claims_loader
def add_claims_to_access_token(accesslevel):
    return {"role": accesslevel}


def create_token(username, accesslevel):

    # Identity can be any data that is json serializable
    new_token = create_access_token(identity=username)
    # add_claims_to_access_token(accesslevel)
    return jsonify(access_token=new_token)


# Protect a view with jwt_required, which requires a valid access token
# in the request to access.
@app.route("/protected", methods=["GET"])
@jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


@app.route("/admin", methods=["GET"])
@admin_required
def admin_func():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


def get_jwt_user():
    return get_jwt_identity()
