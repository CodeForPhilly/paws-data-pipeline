from api.API_ingest import shelterluv_people, salesforce_contacts, sl_animal_events
import structlog

from pipeline.log_db import log_shelterluv_update
logger = structlog.get_logger()

def start():
    logger.debug("Start Fetching raw data from different API sources")

    logger.debug("   Fetching Salesforce contacts")
    salesforce_contacts.store_contacts_all()
    logger.debug("   Finished fetching Salesforce contacts")

    logger.debug("   Fetching Shelterluv people")
    slp_count = shelterluv_people.store_shelterluv_people_all()
    logger.debug("   Finished fetching Shelterluv people - %d records" , slp_count)

    logger.debug("   Fetching Shelterluv events")
    sle_count = sl_animal_events.store_all_animals_and_events()
    logger.debug("   Finished fetching Shelterluv events - %d records" , sle_count)
    log_shelterluv_update()

    logger.debug("Finished fetching raw data from different API sources")

