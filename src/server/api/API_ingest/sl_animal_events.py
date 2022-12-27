import os, time, json
import posixpath as path


import requests

from api.API_ingest import shelterluv_db
from server.api.API_ingest.shelterluv_db import insert_animals

# There are a number of different record types. These are the ones we care about.
keep_record_types = [
    "Outcome.Adoption",
    "Outcome.Foster",
    "Outcome.ReturnToOwner",
    "Intake.AdoptionReturn",
    "Intake.FosterReturn"
]

# from config import engine
# from flask import current_app
# from sqlalchemy.sql import text

BASE_URL = "http://shelterluv.com/api/"
MAX_COUNT = 100  # Max records the API will return for one call

# Get the API key
try:
    from secrets_dict import SHELTERLUV_SECRET_TOKEN
except ImportError:
    # Not running locally
    from os import environ

    try:
        SHELTERLUV_SECRET_TOKEN = environ["SHELTERLUV_SECRET_TOKEN"]
    except KeyError:
        # Not in environment
        # You're SOL for now
        print("Couldn't get SHELTERLUV_SECRET_TOKEN from file or environment")


TEST_MODE=os.getenv("TEST_MODE")  # if not present, has value None

headers = {"Accept": "application/json", "X-API-Key": SHELTERLUV_SECRET_TOKEN}

logger = print  # print to console for testing


# Sample response from events request:

# {
#     "success": 1,
#     "events": [
#         {
#             "Type": "Outcome.Adoption",
#             "Subtype": "PAC",
#             "Time": "1656536900",
#             "User": "phlp_mxxxx",
#             "AssociatedRecords": [
#                 {
#                     "Type": "Animal",
#                     "Id": "5276xxxx"
#                 },
#                 {
#                     "Type": "Person",
#                     "Id": "5633xxxx"
#                 }
#             ]
#         },
#         {...}
#     ],
#     "has_more": true,
#     "total_count": 67467
# }


def get_event_count():
    """Test that server is operational and get total event count."""
    events = "v1/events&offset=0&limit=1"
    URL = path.join(BASE_URL, events)

    try:
        response = requests.request("GET", URL, headers=headers)
    except Exception as e:
        logger("get_event_count failed with ", e)
        return -2

    if response.status_code != 200:
        logger("get_event_count ", response.status_code, "code")
        return -3

    try:
        decoded = json.loads(response.text)
    except json.decoder.JSONDecodeError as e:
        logger("get_event_count JSON decode failed with", e)
        return -4

    if decoded["success"]:
        return decoded["total_count"]
    else:
        logger(decoded['error_message'])
        return -5  # AFAICT, this means URL was bad


def get_events_bulk():
    """Pull all event records from SL """

    # Interesting API design - event record 0 is the newest. But since we pull all records each time it doesn't
    # really matter which direction we go. Simplest to count up, and we can pull until 'has_more' goes false.
    # Good news, the API is robust and won't blow up if you request past the end.
    # At 100 per request, API returns about 5000 records/minute

    event_records = []

    raw_url = path.join(BASE_URL, "v1/events&offset={0}&limit={1}")
    offset = 0
    limit = MAX_COUNT
    more_records = True

    while more_records:

        url = raw_url.format(offset, limit)

        try:
            response = requests.request("GET", url, headers=headers)
        except Exception as e:
            logger("get_events failed with ", e)
            return -2

        if response.status_code != 200:
            logger("get_event_count ", response.status_code, "code")
            return -3

        try:
            decoded = json.loads(response.text)
        except json.decoder.JSONDecodeError as e:
            logger("get_event_count JSON decode failed with", e)
            return -4

        if decoded["success"]:
            for evrec in decoded["events"]:
                if evrec["Type"] in keep_record_types:
                    event_records.append(evrec)

            more_records = decoded["has_more"]  # if so, we'll make another pass
            offset += limit
            if offset % 1000 == 0:
                print("Reading offset ", str(offset))
                if TEST_MODE and offset > 1000:
                    more_records=False  # Break out early 

        else:
            return -5  # AFAICT, this means URL was bad

    return event_records


def slae_test():
    total_count = get_event_count()
    print("Total events:", total_count)

    b = get_events_bulk()
    print("Strored records:", len(b))

    # f = filter_events(b)
    # print(f)

    count = shelterluv_db.insert_events(b)
    return count


# Query to get last adopt/foster event:

# """
#   select 
#      person_id as sl_person_id, max(to_timestamp(time)::date) as last_fosteradopt_event
#  from 
#      sl_animal_events
#  where event_type < 4  -- check this
#  group by 
#      person_id
#  order by 
#     person_id asc;
#    """
# Volgistics last shift 

# """
# select 
#     volg_id, max(from_date) as last_shift
# from
#     volgisticsshifts
# group by 
#     volg_id
# order by   
# volg_id    ;
#     """