from api.API_ingest import shelterluv_api_handler

def start(conn):
    print("Start Fetching raw data from different API sources")
    #Run each source to store the output in dropbox and in the container as a CSV
    shelterluv_api_handler.store_shelterluv_people_all(conn)
    print("Finish Fetching raw data from different API sources")