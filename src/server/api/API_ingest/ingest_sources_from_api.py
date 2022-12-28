import structlog
logger = structlog.get_logger()

from api.API_ingest import shelterluv_api_handler, sl_animal_events

def start(conn):
    logger.debug("Start fetching raw data from different API sources")

    logger.debug("   Fetching Shelterluv people")
    #Run each source to store the output in dropbox and in the container as a CSV
    slp_count = shelterluv_api_handler.store_shelterluv_people_all(conn)
    logger.debug("   Finished fetching Shelterluv people - %d records" , slp_count)

    logger.debug("   Fetching Shelterluv events")
    #Run each source to store the output in dropbox and in the container as a CSV
    sle_count = sl_animal_events.slae_test()
    logger.debug("   Finished fetching Shelterluv events - %d records" , sle_count)

    logger.debug("Finished fetching raw data from different API sources")


    #TODO:   Return object with count for each data source?
