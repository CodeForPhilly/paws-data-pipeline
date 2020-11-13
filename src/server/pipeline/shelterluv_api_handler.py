import requests
import json
import config

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

shelterluv_token = "replace_with_secret_token" #dropbox


''' Iterate over all shelterlove people and store in json file in the raw data folder
We fetch 100 items in each request, since that is the limit based on our research '''
def save_shelterluv_people_all():
    offset = 0
    LIMIT = 100
    has_more = True
    shelterluv_people = []

    while has_more:
        r = requests.get("http://shelterluv.com/api/v1/people?limit={}&offset={}".format(LIMIT, offset),
                         headers={"x-api-key": shelterluv_token})
        response = r.json()
        shelterluv_people += response["people"]
        has_more = response["has_more"]
        offset += 100

    with open(config.RAW_DATA_PATH + "shelterLuv_people.json", "w") as outfile:
        json.dump(shelterluv_people, outfile, indent=4)
