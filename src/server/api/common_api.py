from api.api import common_api
from config import engine
from flask import jsonify
from sqlalchemy.sql import text


@common_api.route('/api/contacts/<search_text>', methods=['GET'])
def get_contacts(search_text):
    with engine.connect() as connection:
        search_text = search_text.lower()

        names = search_text.split(" ")
        if len(names) == 2:
            query = text("select * from pdp_contacts WHERE archived_date is null AND \
                (lower(first_name) like lower(:name1) AND lower(last_name) like lower(:name2) \
                OR lower(first_name) like lower(:name2) AND lower(last_name) like lower(:name1))")
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
        result["shifts"] = []
        result["donations"] = []
        result["adoptions"] = []

        # todo: complete retrieving details for response
        for row in query_result:
            if row["source_type"] == "volgistics":
                query = text("select * from volgisticsshifts where number = :volgistics_id")
                query_result = connection.execute(query, volgistics_id=row["source_id"])
                result["shifts"] += [dict(row) for row in query_result]

        '''
        query = text("select * from salesforcedonations where contact_id = :salesforcecontacts_id")
        query_result = connection.execute(query, salesforcecontacts_id=salesforcecontacts_id)
        salesforcedonations_results = [dict(row) for row in query_result]

        if salesforcedonations_results:
            result['salesforcedonations'] = salesforcedonations_results
        '''

        return jsonify({'result': result})
