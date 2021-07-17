from api.api import common_api
from config import engine
from flask import jsonify
from sqlalchemy.sql import text
import requests
import json
import time
from datetime import datetime
import dateutil.parser


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



from api import jwt_ops


@common_api.route('/api/timeout_test/<duration>', methods=['GET'])
def get_timeout(duration):
    start = datetime.now().strftime("%H:%M:%S");
    time.sleep(int(duration))

    stop = datetime.now().strftime("%H:%M:%S");
    results = jsonify({'result': 'success', 'duration': duration, 'start': start, 'stop': stop})

    return results

@common_api.route('/api/contacts/<search_text>', methods=['GET'])
@jwt_ops.jwt_required()
def get_contacts(search_text):
    with engine.connect() as connection:
        search_text = search_text.lower()

        names = search_text.split(" ")
        if len(names) == 2:
            query = text("select * from pdp_contacts where archived_date is null AND ( \
                (lower(first_name) like lower(:name1) and lower(last_name) like lower(:name2)) \
                OR (lower(first_name) like lower(:name2) and lower(last_name) like lower(:name1)) )\
                    order by lower(last_name), lower(first_name)")
            query_result = connection.execute(query, name1='{}%'.format(names[0]), name2='{}%'.format(names[1]))
        elif len(names) == 1:
            query = text("select * from pdp_contacts \
                WHERE lower(first_name) like lower(:search_text) \
                OR lower(last_name) like lower(:search_text) order by lower(last_name), lower(first_name)")
            query_result = connection.execute(query, search_text='{}%'.format(search_text))

        query_result_json = [dict(row) for row in query_result]

        results = jsonify({'result': query_result_json})

        return results


@common_api.route('/api/360/<matching_id>', methods=['GET'])
@jwt_ops.jwt_required()
def get_360(matching_id):
    result = {}

    with engine.connect() as connection:
        query = text("select * from pdp_contacts where matching_id = :matching_id and archived_date is null")
        query_result = connection.execute(query, matching_id=matching_id)

        result["contact_details"] = [dict(row) for row in query_result]

        for row in result["contact_details"]:
            if row["source_type"] == "salesforcecontacts":
                donations_query = text("""select cast (close_date as text), amount, type,  primary_campaign_source 
                                        from salesforcedonations
                                        where contact_id = :salesforcecontacts_id""")
                salesforce_contacts_query_result = connection.execute(donations_query,
                                                                      salesforcecontacts_id=row["source_id"])
                salesforce_donations_results = [dict(row) for row in salesforce_contacts_query_result]
                result['donations'] = salesforce_donations_results

            if row["source_type"] == "volgistics":
                shifts_query = text("select * from volgisticsshifts where number = :volgistics_id")
                volgistics_shifts_query_result = connection.execute(shifts_query, volgistics_id=row["source_id"])
                volgisticsshifts_results = []

                # todo: temporary fix until formatted in the pipeline
                for r in volgistics_shifts_query_result:
                    shifts = dict(r)
                    # normalize date string
                    if shifts["from_date"]:
                        parsed_date_from = dateutil.parser.parse(shifts["from_date"], ignoretz=True)
                        normalized_date_from = parsed_date_from.strftime("%Y-%m-%d")
                        shifts["from"] = normalized_date_from
                    else:
                        shifts["from"] = "Invalid date"
                    volgisticsshifts_results.append(shifts)

                result['shifts'] = volgisticsshifts_results

            if row["source_type"] == "shelterluvpeople":
                shelterluv_id = row["source_id"]
                result["shelterluv_id"] = shelterluv_id

    return jsonify({'result': result})


@common_api.route('/api/person/<matching_id>/animals', methods=['GET'])
def get_animals(matching_id):
    result = {
        "person_details": {}, 
        "animal_details": {}
    }

    with engine.connect() as connection:
        query = text("select * from pdp_contacts where matching_id = :matching_id and source_type = 'shelterluvpeople' and archived_date is null")
        query_result = connection.execute(query, matching_id=matching_id)
        rows = [dict(row) for row in query_result]
        if len(rows) > 0:
            row = rows[0]
            shelterluv_id = row["source_id"]
            person_url = f"http://shelterluv.com/api/v1/people/{shelterluv_id}"
            person_details = requests.get(person_url, headers={"x-api-key": SHELTERLUV_SECRET_TOKEN}).json()
            result["person_details"]["shelterluv_short_id"] = person_details["ID"]
            animal_ids = person_details["Animal_ids"]
            for animal_id in animal_ids:
                animal_url = f"http://shelterluv.com/api/v1/animals/{animal_id}"
                animal_details = requests.get(animal_url, headers={"x-api-key": SHELTERLUV_SECRET_TOKEN}).json()
                result["animal_details"][animal_id] = animal_details

    return result


@common_api.route('/api/animal/<animal_id>/events', methods=['GET'])
def get_animal_events(animal_id):
    result = {}
    animal_url = f"http://shelterluv.com/api/v1/animals/{animal_id}/events"
    event_details = requests.get(animal_url, headers={"x-api-key": SHELTERLUV_SECRET_TOKEN}).json()
    result[animal_id] = event_details["events"]
    return result


@common_api.route('/api/person/<matching_id>/animal/<animal_id>/events', methods=['GET'])
def get_person_animal_events(matching_id, animal_id):
    result = {}
    events = []
    with engine.connect() as connection:
        query = text("select * from pdp_contacts where matching_id = :matching_id and source_type = 'shelterluvpeople' and archived_date is null")
        query_result = connection.execute(query, matching_id=matching_id)
        rows = [dict(row) for row in query_result]
        if len(rows) > 0:
            row = rows[0]
            shelterluv_id = row["source_id"]
            animal_url = f"http://shelterluv.com/api/v1/animals/{animal_id}/events"
            event_details = requests.get(animal_url, headers={"x-api-key": SHELTERLUV_SECRET_TOKEN}).json()
            for event in event_details["events"]:
                for record in event["AssociatedRecords"]:
                    if record["Type"] == "Person" and record["Id"] == shelterluv_id:
                        events.append(event)
            result[animal_id] = events

    return result

@common_api.route('/api/person/<matching_id>/support', methods=['GET'])
def get_support_oview(matching_id):
    """Return these values for the specified match_id:
        largest gift, date for first donation, total giving, number of gifts,
        amount of first gift, is recurring donor """
    
    # One complication: a single match_id can map to multiple SF ids, so these queries need to 
    # run on a list of of contact_ids.
 
    # First: get the list of contact_ids   
    



    sov_queries = """
                    (SELECT 

                        max(amount) as largest_gift, 
                        min(close_date) as first_donation_date,
                        sum(amount) as total_giving,
                        count(amount) as number_of_gifts

                    FROM
                        salesforcedonations as sfd
                        
                    WHERE
                    contact_id = '0033900002A04BCAAZ')  ;

                    (
                    SELECT 
                        amount as first_gift_amount 
                    FROM
                        salesforcedonations as sfd
                        
                    WHERE
                    contact_id = '0033900002A04BCAAZ'
                    order by close_date asc 
                    limit 1 ) ;

                    (
                    SELECT 
                        recurring_donor as is_recurring
                    FROM
                        salesforcedonations as sfd
                        
                    WHERE
                    contact_id = '0033900002A04BCAAZ'
                    order by close_date DESC 
                    limit 1);
                    """