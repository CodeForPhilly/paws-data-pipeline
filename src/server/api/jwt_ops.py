from functools import wraps
from flask import Flask, jsonify, request, current_app
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    get_jwt_identity,
    verify_jwt_in_request,
    get_jwt
   
)

from app import app, jwt

# Wraps funcs to require admin role to execute
def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims["role"] != "admin":  
            return jsonify(msg="Admins only!"), 403
        else:
            return fn(*args, **kwargs)

    return wrapper

def create_token(username, accesslevel):
    """ Create a JWT *access* token for the specified user ('sub:') and role ('role:'). 
    """
    # Identity can be any data that is json serializable, we just use username
    addl_claims = {'role': accesslevel}
    new_token = create_access_token(identity=username, additional_claims=addl_claims)
    return jsonify(access_token=new_token)


def validate_decode_jwt():
    """ If valid, return jwt fields as a dictionary, else None """
    jwtdict = None
    try:
        jwtdict =  verify_jwt_in_request()[1]
    except:
        pass   # Wasn't valid - either expired or failed validation 

    return jwtdict
