from api import jwt_ops
from api.api import common_api
from config import engine
from flask import jsonify, current_app
from sqlalchemy.sql import text
import requests
import time
from datetime import datetime

try:
    from secrets_dict import SHELTERLUV_SECRET_TOKEN
except ImportError:  # Not running locally
    print("Couldn't get SHELTERLUV_SECRET_TOKEN from file, trying environment") 
    from os import getenv

    SHELTERLUV_SECRET_TOKEN = getenv('SHELTERLUV_SECRET_TOKEN', None)
    if not SHELTERLUV_SECRET_TOKEN:
        print("Couldn't get secrets from file or environment",
            "Defaulting to Fake Data")


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
            query = text("""select pdp_contacts.*, rfm_scores.rfm_score, rfm_label, rfm_color, rfm_text_color
                            from pdp_contacts 
                            left join rfm_scores on rfm_scores.matching_id = pdp_contacts.matching_id
                            left join rfm_mapping on rfm_mapping.rfm_value = rfm_scores.rfm_score
                            where archived_date is null AND ( (lower(first_name) like lower(:name1) and lower(last_name) like lower(:name2)) 
                                OR (lower(first_name) like lower(:name2) and lower(last_name) like lower(:name1)) )
                            order by lower(last_name), lower(first_name)""")
            query_result = connection.execute(query, name1='{}%'.format(names[0]), name2='{}%'.format(names[1]))
        elif len(names) == 1:
            query = text("""select pdp_contacts.*, rfm_scores.rfm_score, rfm_label, rfm_color, rfm_text_color
                            from pdp_contacts 
                            left join rfm_scores on rfm_scores.matching_id = pdp_contacts.matching_id
                            left join rfm_mapping on rfm_mapping.rfm_value = rfm_scores.rfm_score
                            where archived_date is null AND ( lower(first_name) like lower(:search_text) 
                                OR lower(last_name) like lower(:search_text) )
                            order by lower(last_name), lower(first_name)""")
            query_result = connection.execute(query, search_text='{}%'.format(search_text))

        query_result_json = [dict(row) for row in query_result]

        results = jsonify({'result': query_result_json})

        return results


@common_api.route('/api/rfm/<label>/<limit>', methods=['GET'])
@common_api.route('/api/rfm/<label>', methods=['GET'])
@jwt_ops.jwt_required()
def get_rfm(label, limit=None):
    with engine.connect() as connection:
        query_string = """select pdp_contacts.*, rfm_scores.rfm_score, rfm_label, rfm_color, rfm_text_color
                                    from pdp_contacts 
                                    left join rfm_scores on rfm_scores.matching_id = pdp_contacts.matching_id
                                    left join rfm_mapping on rfm_mapping.rfm_value = rfm_scores.rfm_score
                                    where archived_date is null AND rfm_label like :label
                                    and source_type = 'salesforcecontacts'
                                    order by lower(last_name), lower(first_name)"""

        if limit:
            query = text(query_string + " limit :limit")
            query_result = connection.execute(query, label='{}%'.format(label), limit=limit)

        else:
            query = text(query_string)
            query_result = connection.execute(query, label='{}%'.format(label))

        query_result_json = [dict(row) for row in query_result]

        results = jsonify({'result': query_result_json})

        return results


@common_api.route('/api/rfm/labels', methods=['GET'])
@jwt_ops.jwt_required()
def get_rfm_labels():
    with engine.connect() as connection:
        query = text("""select rfm_label, rfm_text_color, rfm_color, count(rfm_value) from rfm_scores left join rfm_mapping on rfm_mapping.rfm_value = rfm_scores.rfm_score 
group by rfm_label, rfm_text_color, rfm_color;""")

        query_result = connection.execute(query)

        query_result_json = [dict(row) for row in query_result]

        results = jsonify({'result': query_result_json})

        return results


@common_api.route('/api/360/<matching_id>', methods=['GET'])
@jwt_ops.jwt_required()
def get_360(matching_id):
    result = {}

    with engine.connect() as connection:
        query = text("""select pdp_contacts.*, rfm_scores.rfm_score, rfm_label, rfm_color, rfm_text_color
                        from pdp_contacts 
                        left join rfm_scores on rfm_scores.matching_id = pdp_contacts.matching_id
                        left join rfm_mapping on rfm_mapping.rfm_value = rfm_scores.rfm_score
                        where pdp_contacts.matching_id = :matching_id and archived_date is null""")
        query_result = connection.execute(query, matching_id=matching_id)

        result["contact_details"] = [dict(row) for row in query_result]

        for row in result["contact_details"]:
            if row["source_type"] == "salesforcecontacts":
                donations_query = text("""select cast (close_date as text), cast (amount as float), donation_type,  primary_campaign_source 
                                        from salesforcedonations
                                        where contact_id = :salesforcecontacts_id""")
                salesforce_contacts_query_result = connection.execute(donations_query,
                                                                      salesforcecontacts_id=row["source_id"])
                salesforce_donations_results = [dict(row) for row in salesforce_contacts_query_result]
                if len(salesforce_donations_results):
                    if not 'donations' in result:
                        result['donations'] = salesforce_donations_results
                    else:
                        result['donations'].append(salesforce_donations_results)

            if row["source_type"] == "volgistics":

                # Shifts data
                shifts_query = text("""select volg_id, assignment, site, from_date, cast(hours as float) 
                                        from volgisticsshifts where volg_id = :volgistics_id
                                        order by from_date desc
                                        limit 5""")
                volgistics_shifts_query_result = connection.execute(shifts_query, volgistics_id=row["source_id"])
                volgisticsshifts_results = []

                for r in volgistics_shifts_query_result:
                    shifts = dict(r)
                    volgisticsshifts_results.append(shifts)

                result['shifts'] = volgisticsshifts_results

                # Volunteer activity
                query_text =  """
                with activity as 
                    (select from_date, hours from volgisticsshifts where volg_id = :volgistics_id),
                alltime as 
                    (select min(from_date) as start_date, sum(hours) as life_hours from activity),
                ytd as 
                    (select sum(hours) as ytd_hours from activity where extract(year from from_date) = extract(year from current_date))
                
                select cast(start_date as text), cast(life_hours as float), cast(ytd_hours as float) from alltime, ytd;
                """
                hours_query = text(query_text)
                hours_query_result = connection.execute(hours_query, volgistics_id=row["source_id"])
                result['activity'] = [dict(row) for row in hours_query_result]

            if row["source_type"] == "shelterluvpeople":
                shelterluv_id = row["source_id"]
                result["shelterluv_id"] = shelterluv_id

    return jsonify({'result': result})


def fake_data(end_point: str)-> dict:
    ''' Takes the end_point as a str of `animals` or `events` and  returns
        a dict representing a test data for that end_point.
    '''

    test_data = {
    'animals': {
        "animal_details": {
            12345: {
                "Age": 24,
                "DOBUnixTime": 1568480456,
                "Name": "Lola aka Fake Cat",
                "Type": "Cat",
                "Photos":
                ["https://images.unsplash.com/photo-1456926631375-92c8ce872def?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8OHx8YW5pbWFsfGVufDB8fDB8fA%3D%3D&w=1000&q=80"],
                "Status": "Healthy In Home",
            },
        },
        "person_details": {
            "shelterluv_short_id": 2,
        },
    },
    'events': {
        12345:[{
                'AssociatedRecords': [
                        {'Id': 12345, 'Type': 'Animal' },
                        {'Id': 12345, 'Type': 'Person'},
                    ],
                'Subtype': 'Foster Home',
                'Time': '1602694822',
                'Type': 'Outcome.Adoption',
                'User': 'Fake User',
            },
        ]
    },
    }

    return test_data.get(end_point, None)


@common_api.route('/api/person/<matching_id>/animals', methods=['GET'])
def get_animals(matching_id):
    result = {
        "person_details": {},
        "animal_details": {}
    }

    if not SHELTERLUV_SECRET_TOKEN:
        return jsonify(fake_data('animals'))

    with engine.connect() as connection:
        query = text("select * from pdp_contacts where matching_id = :matching_id and source_type = 'shelterluvpeople' and archived_date is null")
        query_result = connection.execute(query, matching_id=matching_id)
        rows = [dict(row) for row in query_result]
        if len(rows) > 0:
            for row in rows:
                shelterluv_id = row["source_id"]
                person_url = f"http://shelterluv.com/api/v1/people/{shelterluv_id}"
                person_details = requests.get(person_url, headers={"x-api-key": SHELTERLUV_SECRET_TOKEN}).json()
                if "ID" in person_details:
                    result["person_details"]["shelterluv_short_id"] = person_details["ID"]
                    animal_ids = person_details["Animal_ids"]
                    for animal_id in animal_ids:
                        animal_url = f"http://shelterluv.com/api/v1/animals/{animal_id}"
                        animal_details = requests.get(animal_url, headers={"x-api-key": SHELTERLUV_SECRET_TOKEN}).json()
                        result["animal_details"][animal_id] = animal_details

    return jsonify(result)


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

    if not SHELTERLUV_SECRET_TOKEN:
        return jsonify(fake_data('events'))

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

    return jsonify(result)

@common_api.route('/api/person/<matching_id>/support', methods=['GET'])
def get_support_oview(matching_id):
    """Return these values for the specified match_id:
        largest gift, date for first donation, total giving, number of gifts,
        amount of first gift, is recurring donor 
        
        If consuming this, check number_of_gifts first. If 0, there's no more data
        available, so don't try to read any other fields - they may not exist.
        """

    # One complication: a single match_id can map to multiple SF ids, so these queries need to 
    # run on a list of of contact_ids.

    # First: get the list of salsforce contact_ids associated with the matching_id  
    qcids = text("select source_id FROM pdp_contacts where matching_id = :matching_id and source_type = 'salesforcecontacts';")

    oview_fields = {}

    with engine.connect() as connection:
        query_result = connection.execute(qcids, matching_id=matching_id)
        rows = [dict(row) for row in query_result]

        id_list = []

        if len(rows) > 0:
            for row in rows:
                if row['source_id'].isalnum():
                    id_list.append(row['source_id'])
                else:
                    current_app.logger.warn("salesforcecontacts source_id " + row['source_id'] + "has non-alphanumeric characters; will not be used")

            if len(id_list) == 0: # No ids to query
                oview_fields['number_of_gifts'] = 0    # Marker for no support data
                return jsonify(oview_fields)


            sov1 = text("""SELECT 
                            max(amount) as largest_gift, 
                            min(close_date) as first_donation_date,
                            sum(amount) as total_giving,
                            count(amount) as number_of_gifts
                        FROM
                            salesforcedonations as sfd
                        WHERE
                            contact_id  IN  :id_list  ; """)

            sov1 = sov1.bindparams(id_list=tuple(id_list))
            sov1_result = connection.execute(sov1)

            # query = query.bindparams(values=tuple(values

            # rows = [dict(row) for row in sov1_result]
            row = dict(sov1_result.fetchone())

            if row['largest_gift'] :
                oview_fields['largest_gift'] = float(row['largest_gift'])
            else:
                oview_fields['largest_gift'] = 0.0


            # oview_fields['largest_gift'] = float(rows[0]['largest_gift'])

            if row['first_donation_date']:
                oview_fields['first_donation_date'] = str(row['first_donation_date'])
            else:
                oview_fields['first_donation_date'] = ''

            if row['total_giving']:
                oview_fields['total_giving'] = float(row['total_giving'])
            else:
                oview_fields['total_giving'] = 0.0

            oview_fields['number_of_gifts'] = row['number_of_gifts']


            # These could be could combined them into a single complex query

            sov2 = text("""SELECT 
                                amount as first_gift_amount 
                            FROM
                                salesforcedonations as sfd
                            WHERE
                                contact_id IN :id_list  
                            ORDER BY  close_date asc 
                            limit 1 ; """)

            sov2 = sov2.bindparams(id_list=tuple(id_list))
            sov2_result = connection.execute(sov2)

            if sov2_result.rowcount:
                fga = sov2_result.fetchone()[0]

                if fga:
                    oview_fields['first_gift_amount'] = float(fga)
                else:
                    oview_fields['first_gift_amount'] = 0.0
            else:
                oview_fields['first_gift_amount'] = 0.0

            sov3 = text("""SELECT 
                                recurring_donor as is_recurring
                            FROM
                                salesforcedonations as sfd
                            WHERE
                                contact_id  IN :id_list 
                            ORDER BY close_date DESC 
                            LIMIT  1;  """ )

            sov3 = sov3.bindparams(id_list=tuple(id_list))
            sov3_result = connection.execute(sov3)

            if sov3_result.rowcount:
                oview_fields['is_recurring'] = sov3_result.fetchone()[0]
            else:
                oview_fields['is_recurring'] = False


            rfm = text("""SELECT
                            rfm_score, rfm_color, rfm_label, rfm_text_color
                        FROM 
                            rfm_scores
                            left join rfm_mapping on rfm_mapping.rfm_value = rfm_score
                        WHERE
                            matching_id = :match_id; """)

            rfm = rfm.bindparams(match_id = matching_id)
            rfm_result = connection.execute(rfm)

            if rfm_result.rowcount:
                row = rfm_result.fetchone()
                oview_fields['rfm_score'] = row[0]
                oview_fields['rfm_color'] = row[1]
                oview_fields['rfm_label'] = row[2]                
                oview_fields['rfm_text_color'] = row[3]                

            else:
                oview_fields['rfm_score'] = ''
                oview_fields['rfm_color'] = ''
                oview_fields['rfm_label'] = ''      
                oview_fields['rfm_text_color'] = ''


            return jsonify(oview_fields)


        else:   # len(rows) == 0
            current_app.logger.debug('No SF contact IDs found for matching_id ' + str(matching_id))
            oview_fields['number_of_gifts'] = 0  # Marker for no data
            return jsonify(oview_fields)
