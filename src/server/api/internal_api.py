from datetime import datetime

import structlog
from flask import jsonify, request

from api.API_ingest import ingest_sources_from_api, salesforce_contacts
from api.api import internal_api
from rfm_funcs.create_scores import create_scores
from api.API_ingest import updated_data
from pub_sub import salesforce_message_publisher
import json

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


@internal_api.route("/api/internal/create_scores", methods=["GET"])
def hit_create_scores():
    logger.info("Hitting create_scores() ")
    tuple_count = create_scores()
    logger.info("create_scores()  processed %s scores",  str(tuple_count) )
    return jsonify(200)


@internal_api.route("/api/internal/get_updated_data", methods=["GET"])
def get_contact_data():
    logger.debug("Calling  get_updated_contact_data()")
    contact_json =  updated_data.get_updated_contact_data()
    logger.debug("Returning %d contact records",  len(contact_json) )
    return jsonify(contact_json), 200


@internal_api.route("/api/internal/salesforce_platform_message", methods=["POST"])
def hit_salesforce_platform_message():
    try:
        post_dict = json.loads(request.data)
        salesforce_message_publisher.pipeline_update_message(post_dict)
    except Exception as e:
        logger.error(e)

    return jsonify({'outcome': 'OK'}), 200
