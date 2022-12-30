import requests, os
from models import ShelterluvPeople
import structlog
logger = structlog.get_logger()

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



TEST_MODE=os.getenv("TEST_MODE")  # if not present, has value None
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
def store_shelterluv_people_all(session):
    offset = 0
    LIMIT = 100
    has_more = True

    session.execute("TRUNCATE TABLE shelterluvpeople")

    logger.debug("Start getting shelterluv contacts from people table")

    while has_more:
        r = requests.get("http://shelterluv.com/api/v1/people?limit={}&offset={}".format(LIMIT, offset),
                         headers={"x-api-key": SHELTERLUV_SECRET_TOKEN})
        response = r.json()
        for person in response["people"]:
            #todo: Does this need more "null checks"?
            session.add(ShelterluvPeople(firstname=person["Firstname"],
                                  lastname=person["Lastname"],
                                  id=person["ID"] if "ID" in person else None,
                                  internal_id=person["Internal-ID"],
                                  associated=person["Associated"],
                                  street=person["Street"],
                                  apartment=person["Apartment"],
                                  city=person["City"],
                                  state=person["State"],
                                  zip=person["Zip"],
                                  email=person["Email"],
                                  phone=person["Phone"],
                                  animal_ids=person["Animal_ids"]))
        offset += LIMIT
        has_more = response["has_more"] if not TEST_MODE else response["has_more"] and offset < 1000


    logger.debug("Finish getting shelterluv contacts from people table")

