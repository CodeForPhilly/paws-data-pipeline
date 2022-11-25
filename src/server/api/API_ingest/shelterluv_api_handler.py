import csv
import os
import time

import requests
import pandas as pd
from api.API_ingest.dropbox_handler import upload_file_to_dropbox
from constants import RAW_DATA_PATH
from models import ShelterluvPeople

try:
    from secrets_dict import SHELTERLUV_SECRET_TOKEN
except ImportError:
    # Not running locally
    print("Couldn't get SHELTERLUV_SECRET_TOKEN from file, trying environment **********")
    from os import environ

    try:
        SHELTERLUV_SECRET_TOKEN = environ['SHELTERLUV_SECRET_TOKEN']
    except KeyError:
        # Not in environment
        # You're SOL for now
        print("Couldn't get SHELTERLUV_SECRET_TOKEN from file or environment")


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

    print("Start getting shelterluv contacts from people table")

    while has_more:
        r = requests.get("http://shelterluv.com/api/v1/people?limit={}&offset={}".format(LIMIT, offset),
                         headers={"x-api-key": SHELTERLUV_SECRET_TOKEN})
        response = r.json()
        shelterluv_people += response["people"]
        has_more = response["has_more"]
        offset += 100

    print("Finish getting shelterluv contacts from people table")

    print("Start storing latest shelterluvpeople results to container")
    if os.listdir(RAW_DATA_PATH):
        for file_name in os.listdir(RAW_DATA_PATH):
            file_path = os.path.join(RAW_DATA_PATH, file_name)
            file_name_striped = file_path.split('-')[0].split('/')[-1]

            if file_name_striped == "shelterluvpeople":
                os.remove(file_path)

    file_path = write_csv(shelterluv_people)
    print("Finish storing latest shelterluvpeople results to container")

    print("Start storing " + '/shelterluv/' + "results to dropbox")
    upload_file_to_dropbox(file_path, '/shelterluv/' + file_path.split('/')[-1])
    print("Finish storing " + '/shelterluv/' + "results to dropbox")

    print("Uploading shelterluvpeople csv to database")
    ShelterluvPeople.insert_from_df(pd.read_csv(file_path, dtype="string"), conn)
