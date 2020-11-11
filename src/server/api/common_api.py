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
            query = text("select name, email, master_id as contact_id from user_info \
                where (split_part(lower(name),' ',1) like lower(:name1) and split_part(lower(name),' ',2) like lower(:name2)) \
                OR (split_part(lower(name),' ',1) like lower(:name2) and split_part(lower(name),' ',2) like lower(:name1)) order by name")
            query_result = connection.execute(query, name1='{}%'.format(names[0]), name2='{}%'.format(names[1]))
        elif len(names) == 1:
            query = text("select name, email, master_id as contact_id from user_info \
                WHERE split_part(lower(name),' ',1) like :search_text \
                OR split_part(lower(name),' ',2) like :search_text order by name")
            query_result = connection.execute(query, search_text='{}%'.format(search_text))

        # we only want to display one search result per master id
        id_set  = set()
        results = []
        for result in query_result:
            if result['contact_id'] in id_set:
                continue
            results.append(dict(result))
        results = jsonify({'result': results})

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
        if master_row == None: return
        
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

        #PetPoint
        petpoint_id = master_row['petpoint_id']
        if petpoint_id:
            query = text("select * from petpoint where outcome_person_num = :petpoint_id")
            query_result = connection.execute(query, petpoint_id=petpoint_id)
            petpoint_results = [dict(row) for row in query_result]
            if petpoint_results:
                result['petpoint'] = petpoint_results

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
