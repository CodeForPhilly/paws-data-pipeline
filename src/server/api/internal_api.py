from datetime import datetime

import structlog
from flask import jsonify

from api.API_ingest import ingest_sources_from_api
from api.API_ingest import updated_data
from api.api import internal_api

from pipeline import flow_script
from pub_sub import salesforce_message_publisher


logger = structlog.get_logger()

###   Internal API endpoints can only be accessed from inside the cluster;
###   they are blocked by location rule in NGINX config


# Verify that this can only be accessed from within cluster
@internal_api.route("/api/internal/test", methods=["GET"])
def user_test():
    """ Liveness test, does not require JWT """
    logger.debug("Liveness test")
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


@internal_api.route("/api/internal/get_updated_data", methods=["GET"])
def get_contact_data():
    logger.debug("Calling  get_updated_contact_data()")
    contact_json = updated_data.get_updated_contact_data()
    if contact_json:
        logger.debug("Returning %d contact records", len(contact_json))
    else:
        logger.debug("No contact records found")
    return jsonify({
        'outcome': 'OK',
        'data': contact_json,
        'length': len(contact_json) if contact_json else 0
    }), 200


@internal_api.route("/api/internal/start_flow", methods=["GET"])
def run_flow():
    logger.debug("Calling    flow_script.start_flow()")
    flow_script.start_flow()
    logger.debug("Flow processing complete")
    return jsonify({'outcome': 'OK'}), 200


@internal_api.route("/api/internal/send_salesforce_platform_message", methods=["GET"])
def send_salesforce_platform_message():
    contact_list = updated_data.get_updated_contact_data()
    if contact_list:
        logger.debug("Returning %d contact records", len(contact_list))
        salesforce_message_publisher.send_pipeline_update_messages(contact_list)
    else:
        logger.debug("No contact records found")
    return jsonify({'outcome': 'OK'}), 200

@internal_api.route("/api/internal/full_flow", methods=["GET"])
def start_flow():
    logger.info("Downloading data from APIs")
    ingest_sources_from_api.start()
    logger.info("Starting pipeline matching")
    flow_script.start_flow()
    logger.info("Building updated data payload")
    updated_contacts_list = updated_data.get_updated_contact_data()
    if updated_contacts_list:
        logger.info("Sending Salesforce platform messages")
        salesforce_message_publisher.send_pipeline_update_messages(updated_contacts_list)
    else:
        logger.info("No contacts to update")

    return jsonify({'outcome': 'OK'}), 200