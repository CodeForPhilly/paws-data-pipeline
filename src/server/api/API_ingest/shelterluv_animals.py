import os, time, json
import posixpath as path

import requests

from api.API_ingest import shelterluv_db


# from config import engine
# from flask import current_app
# from sqlalchemy.sql import text

BASE_URL = 'http://shelterluv.com/api/'


try:
    from secrets_dict import SHELTERLUV_SECRET_TOKEN
except ImportError:
    # Not running locally
    from os import environ

    try:
        SHELTERLUV_SECRET_TOKEN = environ['SHELTERLUV_SECRET_TOKEN']
    except KeyError:
        # Not in environment
        # You're SOL for now
        print("Couldn't get SHELTERLUV_SECRET_TOKEN from file or environment")



headers = {
    "Accept": "application/json",
    "X-API-Key": SHELTERLUV_SECRET_TOKEN
}

logger = print

def get_animal_count():
    """Test that server is operational and get total animal count."""
    animals = 'v1/animals&offset=0&limit=1'
    URL = path.join(BASE_URL,animals)

    try:
        response = requests.request("GET",URL, headers=headers)
    except Exception as e:
        logger('get_animal_count failed with ', e)
        return -2

    if response.status_code != 200:
        logger("get_animal_count ", response.status_code, "code")
        return -3

    try:
        decoded = json.loads(response.text)
    except json.decoder.JSONDecodeError as e:
        logger("get_animal_count JSON decode failed with", e)
        return -4

    if decoded['success']:
        return decoded['total_count']
    else:
        return -5   # AFAICT, this means URL was bad


def filter_animals(raw_list):
    """Given a list of animal records as returned by SL, return a list of records with only the fields we care about."""

    good_keys = ['ID', 'Internal-ID', 'Name', 'Type', 'DOBUnixTime', 'CoverPhoto','LastUpdatedUnixTime']

    filtered = []

    for r in raw_list:
        f = {}
        for k in good_keys:
            f[k] = r[k]
        filtered.append(f)

    return filtered




def get_animals_bulk(total_count):
    """Pull all animal records from SL """

    MAX_COUNT = 100  # Max records the API will return for one call

    # 'Great' API design - animal record 0 is the newest, so we need to start at the end, 
    # back up MAX_COUNT rows, make our request, then keep backing up. We need to keep checking
    # the total records to ensure one wasn't added in the middle of the process.
    # Good news, the API is robust and won't blow up if you request past the end.

    raw_url = path.join(BASE_URL, 'v1/animals&offset={0}&limit={1}')

    start_record = total_count -1
    offset = (start_record - MAX_COUNT)  if  (start_record - MAX_COUNT) > -1  else 0

    while offset > -1 :

        url = raw_url.format(offset,MAX_COUNT)

        try:
            response = requests.request("GET",url, headers=headers)
        except Exception as e:
            logger('get_animals failed with ', e)
            return -2

        if response.status_code != 200:
            logger("get_animal_count ", response.status_code, "code")
            return -3

        try:
            decoded = json.loads(response.text)
        except json.decoder.JSONDecodeError as e:
            logger("get_animal_count JSON decode failed with", e)
            return -4

        if decoded['success']:
            return decoded['animals']
        else:
            return -5   # AFAICT, this means URL was bad




def sla_test():
    total_count = get_animal_count()
    print('Total animals:',total_count)

    b = get_animals_bulk(200)
    print(len(b))

    f = filter_animals(b)
    print(f)

    count = shelterluv_db.insert_animals(f)
    return count


# if __name__ == '__main__' :    

#     total_count = get_animal_count()
#     print('Total animals:',total_count)

#     b = get_animals_bulk(9)
#     print(len(b))

#     f = filter_animals(b)
#     print(f)

#     count = shelterluv_db.insert_animals(f)