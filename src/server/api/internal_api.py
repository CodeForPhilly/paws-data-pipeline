from datetime import datetime

import structlog
from flask import jsonify

from api.API_ingest import ingest_sources_from_api
from api.api import internal_api

logger = structlog.get_logger()

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


@internal_api.route("/api/internal/ingestRawData", methods=["GET"])
def ingest_raw_data():
    try:
        ingest_sources_from_api.start()
    except Exception as e:
        logger.error(e)

    return jsonify({'outcome': 'OK'}), 200


