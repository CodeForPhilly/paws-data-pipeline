from api.API_ingest import shelterluv_api_handler, sl_animal_events

def start(conn):
    print("Start fetching raw data from different API sources")

    print("   Fetching Shelterluv people")
    #Run each source to store the output in dropbox and in the container as a CSV
    slp_count = shelterluv_api_handler.store_shelterluv_people_all(conn)
    print("   Finished fetching Shelterluv people - %d records" % slp_count)

    print("   Fetching Shelterluv events")
    #Run each source to store the output in dropbox and in the container as a CSV
    sle_count = sl_animal_events.slae_test()
    print("   Finished fetching Shelterluv events - %d records" % sle_count)

    print("Finished fetching raw data from different API sources")


    #TODO:   Return object with count for each data source?
