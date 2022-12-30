from api.api import internal_api
from config import engine
from flask import jsonify, current_app
from datetime import datetime
from api.API_ingest import ingest_sources_from_api
from rfm_funcs.create_scores import create_scores
from sqlalchemy.orm import  sessionmaker

import structlog
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
        Session = sessionmaker(engine)
        with Session() as session:
            ingest_sources_from_api.start(session)
            session.commit()
    except Exception as e:
        logger.error(e)

    return jsonify({'outcome': 'OK'}), 200


@internal_api.route("/api/internal/create_scores", methods=["GET"])
def hit_create_scores():
    logger.info("Hitting create_scores() ")
    tuple_count = create_scores()
    logger.info("create_scores()  processed %s scores",  str(tuple_count) )
    return jsonify(200)
