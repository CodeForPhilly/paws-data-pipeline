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


@jwt.user_claims_loader
def add_claims_to_access_token(accesslevel):
    """ Adds role k/v to token """
    return {"role": accesslevel}


def create_token(username, accesslevel):
    """ Create a JWT *access* token for the specified user and role. 
        Role is magically added by the user_claims_loader decorator 
    """
    # Identity can be any data that is json serializable
    new_token = create_access_token(identity=username)
    # add_claims_to_access_token(accesslevel)
    return jsonify(access_token=new_token)


def get_jwt_user():
    """ Read the JWT and return the associated username """
    return get_jwt_identity()
