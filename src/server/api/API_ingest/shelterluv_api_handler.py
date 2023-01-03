import csv
import os
import time

import requests
import pandas as pd
from api.API_ingest.dropbox_handler import upload_file_to_dropbox
from constants import RAW_DATA_PATH
from models import ShelterluvPeople
import structlog
logger = structlog.get_logger()


TEST_MODE = os.getenv("TEST_MODE")

try:
    from secrets_dict import SHELTERLUV_SECRET_TOKEN
except ImportError:
    # Not running locally
    logger.debug("Couldn't get SHELTERLUV_SECRET_TOKEN from file, trying environment **********")
    from os import environ

    try:
        SHELTERLUV_SECRET_TOKEN = environ['SHELTERLUV_SECRET_TOKEN']
    except KeyError:
        # Not in environment
        # You're SOL for now
        logger.error("Couldn't get SHELTERLUV_SECRET_TOKEN from file or environment")


def write_csv(json_data):
    now = time.localtime()
    now_date = time.strftime("%Y-%m-%d--%H-%M-%S", now)

    path = RAW_DATA_PATH + "shelterluvpeople-" + now_date + ".csv"  # store file name to use for dropbox

    file_handle = open(path, "w")

    csv_writer = csv.writer(file_handle)

    count = 0
    for item in json_data:
        if count == 0:
            # Writing headers of CSV file
            header = item.keys()
            csv_writer.writerow(header)
            count += 1

        # Writing data of CSV file
        csv_writer.writerow(item.values())

    file_handle.close()

    return path

#################################
# This script is used to fetch data from shelterluv API.
# Please be mindful of your usage.
# example: /people will fetch the data of all people. and send approximately 300 requests.
# https://help.shelterluv.com/hc/en-us/articles/115000580127-Shelterluv-API-Overview
#################################

######## Insights ###############
# Max result items is 100 - even though it's not specifically specified in the above reference
# /people has all the data. it seems that /person/:id isn't used
#################################

''' Iterate over all shelterlove people and store in json file in the raw data folder
We fetch 100 items in each request, since that is the limit based on our research '''
def store_shelterluv_people_all(conn):
    offset = 0
    LIMIT = 100
    has_more = True
    shelterluv_people = []

    logger.debug("Start getting shelterluv contacts from people table")

    while has_more:
        r = requests.get("http://shelterluv.com/api/v1/people?limit={}&offset={}".format(LIMIT, offset),
                         headers={"x-api-key": SHELTERLUV_SECRET_TOKEN})
        response = r.json()
        shelterluv_people += response["people"]
        has_more = response["has_more"]
        offset += 100

        if offset % 1000 == 0:
            print("Reading offset ", str(offset))
            if TEST_MODE and offset > 1000:
                has_more=False  # Break out early 



    print("Finish getting shelterluv contacts from people table")

    logger.debug("Start storing latest shelterluvpeople results to container")
    if os.listdir(RAW_DATA_PATH):
        for file_name in os.listdir(RAW_DATA_PATH):
            file_path = os.path.join(RAW_DATA_PATH, file_name)
            file_name_striped = file_path.split('-')[0].split('/')[-1]

            if file_name_striped == "shelterluvpeople":
                os.remove(file_path)

    file_path = write_csv(shelterluv_people)
    logger.debug("Finish storing latest shelterluvpeople results to container")

    logger.debug("Start storing " + '/shelterluv/' + "results to dropbox")
    upload_file_to_dropbox(file_path, '/shelterluv/' + file_path.split('/')[-1])
    logger.debug("Finish storing " + '/shelterluv/' + "results to dropbox")

    logger.debug("Uploading shelterluvpeople csv to database")
    ShelterluvPeople.insert_from_df(pd.read_csv(file_path, dtype="string"), conn)

    return offset
