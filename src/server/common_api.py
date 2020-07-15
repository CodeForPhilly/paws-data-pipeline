from config import engine
from server.api import common_api
from flask import jsonify
from sqlalchemy.sql import text


@common_api.route('/contacts/<search_text>', methods=['GET'])
def get_contacts(search_text):
    with engine.connect() as connection:
        #todo: add logic to grab names from all sources - 1.salesforce 2.volgistics 3.petpoint once you find one, return all unique names and email
        query = text("select concat(first_name,' ',last_name) as name, email, contact_id from salesforcecontacts \
            WHERE lower(first_name) like :search_text \
            OR lower(last_name) like :search_text")
        query_result = connection.execute(query, search_text='%{}%'.format(search_text.lower()))

        results = jsonify({'result': [dict(row) for row in query_result]})

        return results


@common_api.route('/360/<salesforce_id>', methods=['GET'])
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

        query_result = connection.execute(
            "select * from petpoint where outcome_person_num='{}'".format(master_row['result'][0]['petpoint_id']))
        petpoint_results = [dict(row) for row in query_result]
        if petpoint_results:
            result['petpoint'] = petpoint_results[0]
        
        query_result = connection.execute(
            "select * from volgistics where number='{}'".format(master_row['result'][0]['volgistics_id']))
        volgistics_results = [dict(row) for row in query_result]
        if volgistics_results:
            result['volgistics'] = volgistics_results[0]

        return jsonify(result)
