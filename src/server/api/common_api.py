from api.api import common_api
from config import engine
from flask import jsonify
from sqlalchemy.sql import text


@common_api.route('/api/contacts/<search_text>', methods=['GET'])
def get_contacts(search_text):
    with engine.connect() as connection:
        search_text = search_text.lower()

        #TODO: Is the client expecting the id labeled as contact_id?
        names = search_text.split(" ")
        if len(names) == 2:
            query = text("select * from pdp_contacts \
                where lower(first_name) like lower(:name1) and lower(last_name) like lower(:name2) \
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


@common_api.route('/api/360/<master_id>', methods=['GET'])
def get_360(master_id):
    result = {}

    with engine.connect() as connection:
        #Master Table
        query = text("select * from master where _id = :master_id")
        query_result = connection.execute(query, master_id=master_id)
        #todo: this shouldn't loop so eliminate the for
        master_row = query_result.fetchone()

        if master_row:
            #Salesforce
            salesforcecontacts_id = master_row['salesforcecontacts_id']

            if salesforcecontacts_id:
                query = text("select * from salesforcecontacts where contact_id = :salesforcecontacts_id")
                query_result = connection.execute(query, salesforcecontacts_id=salesforcecontacts_id)
                salesforce_results = [dict(row) for row in query_result]

                if salesforce_results:
                    result['salesforcecontacts'] = salesforce_results[0]

                query = text("select * from salesforcedonations where contact_id = :salesforcecontacts_id")
                query_result = connection.execute(query, salesforcecontacts_id=salesforcecontacts_id)
                salesforcedonations_results = [dict(row) for row in query_result]

                if salesforcedonations_results:
                    result['salesforcedonations'] = salesforcedonations_results

            #Shelterluv
            shelterluvpeople_id = master_row['shelterluvpeople_id']

            if shelterluvpeople_id:
                query = text("select * from shelterluvpeople where id = :shelterluvpeople_id")
                query_result = connection.execute(query, shelterluvpeople_id=shelterluvpeople_id)
                shelterluvpeople_results = [dict(row) for row in query_result]

                if shelterluvpeople_results:
                    result['shelterluvpeople'] = shelterluvpeople_results

            #Volgistics
            volgistics_id = master_row['volgistics_id']

            if volgistics_id:
                query = text("select * from volgistics where number = :volgistics_id")
                query_result = connection.execute(query, volgistics_id=volgistics_id)
                volgistics_results = [dict(row) for row in query_result]

                query = text("select * from volgisticsshifts where number = :volgistics_id")
                query_result = connection.execute(query, volgistics_id=volgistics_id)
                volgistics_shifts_results = [dict(row) for row in query_result]

                if volgistics_results:
                    result['volgistics'] = volgistics_results[0]
                    result['volgistics_shifts_results'] = volgistics_shifts_results

            return jsonify(result)
