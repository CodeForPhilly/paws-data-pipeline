from api.API_ingest import shelterluv_people, salesforce_contacts
import structlog
logger = structlog.get_logger()

def start(session):
    logger.debug("Start Fetching raw data from different API sources")
    #Run each source to store the output in dropbox and in the container as a CSV
    shelterluv_people.store_shelterluv_people_all(session)
    salesforce_contacts.store_contacts_all(session)
    logger.debug("Finish Fetching raw data from different API sources")
    slp_count = shelterluv_api_handler.store_shelterluv_people_all(conn)
    logger.debug("   Finished fetching Shelterluv people - %d records" , slp_count)

    logger.debug("   Fetching Shelterluv events")
    #Run each source to store the output in dropbox and in the container as a CSV
    sle_count = sl_animal_events.slae_test()
    logger.debug("   Finished fetching Shelterluv events - %d records" , sle_count)

    logger.debug("Finished fetching raw data from different API sources")


    #TODO:   Return object with count for each data source?
