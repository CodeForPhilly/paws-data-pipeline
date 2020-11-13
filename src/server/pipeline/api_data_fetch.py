import requests
import json
import config

#################################
# This script is used to fetch data from shelterluv API.
# Please be mindful of your usage.
# example: /people will fetch the data of all people. and send approximately 300 requests.
#################################

shelterluv_token = "replace_with_secret_token" #dropbox
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
