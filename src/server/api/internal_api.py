from api.api import internal_api
from config import db
from flask import jsonify, current_app
from datetime import datetime
from api.API_ingest import ingest_sources_from_api
from rfm_funcs.create_scores import create_scores

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


@internal_api.route("/api/ingestRawData", methods=["GET"])
def ingest_raw_data():
    try:
        with db.engine.begin() as conn:
            ingest_sources_from_api.start(conn)
    except Exception as e:
        current_app.logger.exception(e)

    return jsonify({'outcome': 'OK'}), 200


@internal_api.route("/api/internal/create_scores", methods=["GET"])
def hit_create_scores():
    current_app.logger.info("Hitting create_scores() ")
    tuple_count = create_scores()
    current_app.logger.info("create_scores()  processed " + str(tuple_count) + " scores")
    return jsonify(200)
