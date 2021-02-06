from api.api import common_api
from config import engine
from flask import jsonify
from sqlalchemy.sql import text
import requests
import json
import dateutil.parser
from secrets import SHELTERLUV_SECRET_TOKEN


@common_api.route('/api/contacts/<search_text>', methods=['GET'])
def get_contacts(search_text):
    with engine.connect() as connection:
        search_text = search_text.lower()

        names = search_text.split(" ")
        if len(names) == 2:
            query = text("select * from pdp_contacts where archived_date is null AND\
                lower(first_name) like lower(:name1) and lower(last_name) like lower(:name2) \
                OR lower(first_name) like lower(:name2) and lower(last_name) like lower(:name1)")
            query_result = connection.execute(query, name1='{}%'.format(names[0]), name2='{}%'.format(names[1]))
        elif len(names) == 1:
            query = text("select * from pdp_contacts \
                WHERE lower(first_name) like lower(:search_text) \
                OR lower(last_name) like lower(:search_text)")
            query_result = connection.execute(query, search_text='{}%'.format(search_text))

        query_result_json = [dict(row) for row in query_result]

        results = jsonify({'result': query_result_json})

        return results


@common_api.route('/api/360/<matching_id>', methods=['GET'])
def get_360(matching_id):
    result = {}

    with engine.connect() as connection:
        query = text("select * from pdp_contacts where matching_id = :matching_id and archived_date is null")
        query_result = connection.execute(query, matching_id=matching_id)

        result["contact_details"] = [dict(row) for row in query_result]

        for row in result["contact_details"]:
            if row["source_type"] == "salesforcecontacts":
                donations_query = text("select * from salesforcedonations where contact_id like :salesforcecontacts_id")
                salesforce_contacts_query_result = connection.execute(donations_query,
                                                                      salesforcecontacts_id=row["source_id"] + "%")
                salesforce_donations_results = [dict(row) for row in salesforce_contacts_query_result]
                result['donations'] = salesforce_donations_results

            if row["source_type"] == "volgistics":
                shifts_query = text("select * from volgisticsshifts where number = :volgistics_id")
                volgistics_shifts_query_result = connection.execute(shifts_query, volgistics_id=row["source_id"])
                volgisticsshifts_results = []
                for r in volgistics_shifts_query_result:
                    shifts = dict(r)
                    # normalize date string
                    parsed_date_from = dateutil.parser.parse(shifts["from"], ignoretz=True)
                    normalized_date_from = parsed_date_from.strftime("%Y-%m-%d")
                    shifts["from"] = normalized_date_from
                    volgisticsshifts_results.append(shifts)
                
                result['shifts'] = volgisticsshifts_results

            if row["source_type"] == "shelterluvpeople":
                adoptions = []
                person = requests.get("http://shelterluv.com/api/v1/people/{}".format(row["source_id"]),
                                      headers={"x-api-key": SHELTERLUV_SECRET_TOKEN})
                person_json = person.json()
                animal_ids = person_json["Animal_ids"]

                for animal_id in animal_ids:
                    animal_events = requests.get("http://shelterluv.com/api/v1/animals/{}/events".format(animal_id),
                                                 headers={"x-api-key": SHELTERLUV_SECRET_TOKEN})
                    animal_events_json = animal_events.json()

                    for event in animal_events_json["events"]:
                        for adoption in event["AssociatedRecords"]:
                            if adoption["Type"] == "Person" and adoption["Id"] == row["source_id"]:
                                del event["AssociatedRecords"]
                                animal_details = requests.get(
                                    "http://shelterluv.com/api/v1/animals/{}".format(animal_id),
                                    headers={"x-api-key": SHELTERLUV_SECRET_TOKEN})

                                animal_details_json = animal_details.json()
                                event["animal_details"] = animal_details_json
                                adoptions.append(event)

                    result['adoptions'] = adoptions

        return jsonify({'result': result})
