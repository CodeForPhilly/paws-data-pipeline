from config import engine
from server.api import common_api
from flask import jsonify


@common_api.route('/salesforcecontacts', methods=['GET'])
def get_contacts():
    with engine.connect() as connection:
        query_result = connection.execute(
            "select concat(first_name,' ',last_name) as name, email, contact_id from salesforcecontacts")

        results = jsonify({'result': [dict(row) for row in query_result]})

        return results


@common_api.route('/360/<salesforce_id>', methods=['GET'])
def get_360(salesforce_id):
    result = {
        'salesforcecontacts': None
    }

    with engine.connect() as connection:
        query_result = connection.execute(
            "select * from master where salesforce_id='{}'".format(salesforce_id))

        master_row = {'result': [dict(row) for row in query_result]}

        query_result = connection.execute(
            "select * from salesforcecontacts where contact_id='{}'".format(salesforce_id))
        result['salesforcecontacts'] = [dict(row) for row in query_result][0]

        query_result = connection.execute(
            "select * from petpoint where outcome_person_='{}'".format(master_row['result'][0]['petpoint_id']))
        result['petpoint'] = [dict(row) for row in query_result][0]

        query_result = connection.execute(
            "select * from volgistics where number='{}'".format(master_row['result'][0]['volgistics_id']))
        result['volgistics'] = [dict(row) for row in query_result][0]

        return jsonify(result)
