from api.API_ingest import shelterluv_api_handler, salesforce_api_handler
import structlog
logger = structlog.get_logger()

def start(session):
    logger.debug("Start Fetching raw data from different API sources")
    #Run each source to store the output in dropbox and in the container as a CSV
    shelterluv_api_handler.store_shelterluv_people_all(session)
    salesforce_api_handler.store_contacts_all(session)
    logger.debug("Finish Fetching raw data from different API sources")