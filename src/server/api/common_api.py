from config import engine
from api.api import common_api
from flask import jsonify
from sqlalchemy.sql import text


@common_api.route('/api/contacts/<search_text>', methods=['GET'])
def get_contacts(search_text):
    with engine.connect() as connection:
        search_text = search_text.lower()

        names = search_text.split(" ")
        if len(names) == 2:
            first_name = names[1]
            last_name = names[0]
            # note: query is an AND and the first name starts with the value 
            query = text("select concat(first_name,' ',last_name) as name, email, contact_id from salesforcecontacts \
                WHERE lower(first_name) like :first_name \
                AND lower(last_name) like :last_name order by last_name")
            query_result = connection.execute(query, first_name='{}%'.format(first_name), last_name='%{}%'.format(last_name))
        else:
            #todo: add logic to grab names from all sources - 1.salesforce 2.volgistics 3.petpoint once you find one, return all unique names and email
            query = text("select concat(first_name,' ',last_name) as name, email, contact_id from salesforcecontacts \
                WHERE lower(first_name) like :search_text \
                OR lower(last_name) like :search_text order by last_name")
            query_result = connection.execute(query, search_text='%{}%'.format(search_text))

        results = jsonify({'result': [dict(row) for row in query_result]})

        return results


@common_api.route('/api/360/<salesforce_id>', methods=['GET'])
def get_360(salesforce_id):
    result = {}

    with engine.connect() as connection:
        query_result = connection.execute(
            "select * from master where salesforcecontacts_id='{}'".format(salesforce_id))
        master_row = {'result': [dict(row) for row in query_result]}

        query_result = connection.execute(
            "select * from salesforcecontacts where contact_id='{}'".format(salesforce_id))
        salesforce_results = [dict(row) for row in query_result]
        if salesforce_results:
            result['salesforcecontacts'] = salesforce_results[0]

        if master_row['result']:
            petpoint_results = []

            for item in master_row['result']:
                query_result = connection.execute(
                    "select * from petpoint where outcome_person_num='{}'".format(item['petpoint_id']))

                petpoint_results = [dict(row) for row in query_result]

            if petpoint_results:
                result['petpoint'] = petpoint_results

        if master_row['result']:
            query_result = connection.execute(
                "select * from volgistics where number='{}'".format(master_row['result'][0]['volgistics_id']))

            volgistics_results = [dict(row) for row in query_result]

            query_result = connection.execute(
                "select * from volgisticsshifts where number='{}'".format(master_row['result'][0]['volgistics_id']))

            volgistics_shifts_results = [dict(row) for row in query_result]

            if volgistics_results:
                result['volgistics'] = volgistics_results[0]
                result['volgistics_shifts_results'] = volgistics_shifts_results

        return jsonify(result)
