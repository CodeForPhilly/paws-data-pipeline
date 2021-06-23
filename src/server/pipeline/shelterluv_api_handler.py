import requests
import csv
from config import RAW_DATA_PATH

try:   
    from secrets import SHELTERLUV_SECRET_TOKEN
except ImportError:   
    # Not running locally
    print("Couldn't get SL_TOKEN from file, trying environment **********")
    from os import environ

    try:
        SHELTERLUV_SECRET_TOKEN = environ['SHELTERLUV_SECRET_TOKEN']
    except KeyError:
        # Nor in environment
        # You're SOL for now
        print("Couldn't get secrets from file or environment")


def write_csv(json_data):
    result = open(RAW_DATA_PATH + "shelterluv_people.csv", "w")

    csv_writer = csv.writer(result)
    count = 0

    for item in json_data:
        if count == 0:
            # Writing headers of CSV file
            header = item.keys()
            csv_writer.writerow(header)
            count += 1

        # Writing data of CSV file
        csv_writer.writerow(item.values())

    result.close()

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
def store_shelterluv_people_all():
    offset = 0
    LIMIT = 100
    has_more = True
    shelterluv_people = []

    while has_more:
        r = requests.get("http://shelterluv.com/api/v1/people?limit={}&offset={}".format(LIMIT, offset),
                         headers={"x-api-key": SHELTERLUV_SECRET_TOKEN})
        response = r.json()
        shelterluv_people += response["people"]
        has_more = response["has_more"]
        offset += 100

    write_csv(shelterluv_people)


if __name__ == "__main__":
    # execute only if run as a script
    store_shelterluv_people_all()