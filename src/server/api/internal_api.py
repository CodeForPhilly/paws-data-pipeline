
from api.api import internal_api
from flask import request, redirect, jsonify, current_app, abort, json
from datetime import datetime


###   Internal API endpoints can only be accessed from inside the cluster;
###   they are blocked by location rule in NGINX config


# Verify that this can only be accessed from within cluster
@internal_api.route("/api/internal/test", methods=["GET"])
def user_test():
    """ Liveness test, does not require JWT """
    return jsonify(("OK from INTERNAL Test  @ " + str(datetime.now())))

@internal_api.route("/api/internal/test/test", methods=["GET"])
def user_test2():
    """ Liveness test, does not require JWT """
    return jsonify(("OK from INTERNAL test/test  @ " + str(datetime.now())))