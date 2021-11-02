from api.api import admin_api
import os
import time
from datetime import datetime
import json
from sqlalchemy.sql import text

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import Table, MetaData
from pipeline import flow_script
from config import engine
from flask import request, redirect, jsonify, current_app
from api.file_uploader import validate_and_arrange_upload
from sqlalchemy.orm import Session, sessionmaker

from api import jwt_ops
from config import RAW_DATA_PATH

ALLOWED_EXTENSIONS = {"csv", "xlsx"}


def __allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# file upload tutorial
@admin_api.route("/api/file", methods=["POST"])
@jwt_ops.admin_required
def upload_csv():
    for file in request.files.getlist("file"):
        if __allowed_file(file.filename):
            try:
                validate_and_arrange_upload(file)
            except Exception as e:
                current_app.logger.exception(e)
            finally:
                file.close()

    return redirect(request.origin)


@admin_api.route("/api/listCurrentFiles", methods=["GET"])
@jwt_ops.admin_required
def list_current_files():
    result = None

    current_app.logger.info("Start returning file list")
    file_list_result = os.listdir(RAW_DATA_PATH)

    if len(file_list_result) > 0:
        result = file_list_result

    return jsonify(result)


@admin_api.route("/api/execute", methods=["POST"])
@jwt_ops.admin_required
def execute():
    current_app.logger.info("Execute flow")
    job_outcome = flow_script.start_flow() # 'busy', 'completed', or 'nothing to do'
    current_app.logger.info("Job outcome: " + str(job_outcome))


    # --------   Skip update if 'busy' or 'nothing to do' as nothing changed ? ------
    current_time = datetime.now().ctime()
    statistics = get_statistics()

    last_execution_details = {"executionTime": current_time, "stats": statistics}
    last_ex_json = (json.dumps(last_execution_details))
    
    metadata = MetaData()
    kvt = Table("kv_unique", metadata, autoload=True, autoload_with=engine)

    # Write Last Execution stats to DB
    # See Alembic Revision ID: 05e0693f8cbb for table definition
    with engine.connect() as connection:
        ins_stmt = insert(kvt).values(               # Postgres-specific insert() supporting ON CONFLICT
            keycol = 'last_execution_time',
            valcol = last_ex_json,
            )
        # If key already present in DB, do update instead
        upsert = ins_stmt.on_conflict_do_update(
                constraint='kv_unique_keycol_key',
                set_=dict(valcol=last_ex_json)
                )

        try:
            connection.execute(upsert)
        except Exception as e:
            current_app.logger.error("Insert/Update failed on Last Execution stats")
            current_app.logger.exception(e)
    # -------------------------------------------------------------------------------
    
    if job_outcome == 'busy':
        return jsonify({'outcome' : 'Already analyzing'}), 503   

    elif job_outcome == 'nothing to do':
        return jsonify({'outcome' : 'No uploaded files to process'}), 200

    elif job_outcome == 'completed' :
        return jsonify({'outcome' : 'Analysis completed'}), 200

    elif job_outcome == 'error' :
        return jsonify({'outcome' : 'Analysis not completed due to error'}), 500
    
    else:
        return jsonify({'outcome' : 'Unknown status: ' + str(job_outcome)}), 200


def get_statistics():
    with engine.connect() as connection:
        query_matches = text("SELECT count(*) FROM (SELECT distinct matching_id from pdp_contacts) as a;")
        query_total_count = text("SELECT count(*) FROM pdp_contacts;")
        matches_count_query_result = connection.execute(query_matches)
        total_count_query_result = connection.execute(query_total_count)

        # Need to iterate over the results proxy
        results = {
            "Distinct Matching Groups Count": [dict(row) for row in matches_count_query_result][0]["count"],
            "Total Contacts Count": [dict(row) for row in total_count_query_result][0]["count"]
        }

        return results


@admin_api.route("/api/statistics", methods=["GET"])
@jwt_ops.admin_required
def list_statistics():
    """ Pull Last Execution stats from DB. """
    current_app.logger.info("list_statistics() request")
    last_execution_details = '{}'  # Empty but valid JSON

    engine.dispose() # we don't want other process's conn pool


    with engine.connect() as conn:
    
        try:    # See Alembic Revision ID: 05e0693f8cbb for table definition
        
            s = text("select valcol from kv_unique where keycol = 'last_execution_time';")
            result = conn.execute(s)
            if result.rowcount > 0:
                last_execution_details = result.fetchone()[0]

        except Exception as e:
            current_app.logger.error("Failure reading Last Execution stats from DB - OK on first run")
        # Will happen on first run, shouldn't after 

    return last_execution_details


@admin_api.route("/api/get_execution_status", methods=["GET"])
@jwt_ops.admin_required
def get_exec_status():
    """ Get the execution status record from the DB for a running job, if present"""


    engine.dispose() # we don't want other process's conn pool

    with engine.connect() as connection:
        q = text("""SELECT job_id, stage, status, details, update_stamp 
                    FROM execution_status 
                    WHERE status = 'executing' """)
        result = connection.execute(q)

        if result.rowcount > 0:
           running_job = result.fetchone()
           return jsonify(dict(zip(result.keys(), running_job)))
        else:
            return jsonify('')

@admin_api.route("/api/job_in_progress", methods=["GET"])
@jwt_ops.admin_required
def is_job_in_progresss():
    """Return True if there's a running execute, False if not. """

    engine.dispose() # we don't want other process's conn pool

    with engine.connect() as connection:
        q = text("""SELECT job_id from execution_status WHERE status = 'executing' """)
        result = connection.execute(q)

        if result.rowcount > 0:
            return jsonify(True)
        else:
            return jsonify(False)


def start_job():
    """If no running jobs, create a job_id and execution status entry.
    This ensures only only one job runs at a time.
    If there's a running job, return None.  """


    engine.dispose() # we don't want other process's conn pool

    job_id = str(int(time.time()))
    q = text("""SELECT job_id from execution_status
                    WHERE status = 'executing' """)

    i = text("""INSERT INTO execution_status (job_id, stage, status, details) 
                values(:j, :stg, :stat, :det) """)
    i = i.bindparams(j = job_id, 
                     stg ='initiating',
                     stat ='executing',
                     det = ''   )

    running_job = None

    with engine.begin() as connection:   # BEGIN TRANSACTION
        q_result = connection.execute(q)
        if q_result.rowcount == 0:
            # No running jobs
            ins_result = connection.execute(i)
        else:
            running_job = q_result.fetchone()[0]
    # COMMIT TRANSACTION
    #TODO: what would an exception look like here? 


    if running_job :
        # There was a running job already
        current_app.logger.info("Request to start job, but job_id " + str(running_job) + " already executing")
        return None
    else:
        current_app.logger.info("Assigned job_id " + job_id )
        return job_id



def insert_rfm_scores(score_list):
    """Take a list of (matching_id, score) and insert into the
        rfm_scores table.
    """
            # This takes about 4.5 sec to insert 80,000 rows 

    Session = sessionmaker(engine) 
    session =  Session()   
    metadata = MetaData()
    rfms = Table("rfm_scores", metadata, autoload=True, autoload_with=engine)


    truncate = "TRUNCATE table rfm_scores;"
    result = session.execute(truncate)

    ins_list = []   # Create a list of per-row dicts
    for pair in score_list:
        ins_list.append( {'matching_id' : pair[0], 'rfm_score' : pair[1]} )


    ret = session.execute(rfms.insert(ins_list))

    session.commit()   # Commit all inserted rows
    session.close()

    return ret.rowcount


# This is super-hacky - temporary
@admin_api.route("/api/import_rfm", methods=["GET"])
def  import_rfm_csv():
    """ This imports the CSV files and calls the insert function"""
    import csv

    score_list = []

    #  Put your local file location \/

    with open('C:\\Projects\\paws-stuff\\score_tuples.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        hdr = next(reader)
        print('Skipping header: ', hdr)
        for row in reader:
            score_list.append(row)

    rc = insert_rfm_scores(score_list)

    return str(rc) + " rows inserted"


def write_rfm_edges(rfm_dict : dict) :
    """Write the rfm edge dictionary to the DB"""

    if len(rfm_dict) == 3 :  #  R, F, *and* M!
        rfm_s = json.dumps(rfm_dict)  # Convert dict to string

        metadata = MetaData()
        kvt = Table("kv_unique", metadata, autoload=True, autoload_with=engine)

        # See Alembic Revision ID: 05e0693f8cbb for table definition
        with engine.connect() as connection:
            ins_stmt = insert(kvt).values(               # Postgres-specific insert() supporting ON CONFLICT
                keycol = 'rfm_edges',
                valcol = rfm_s,
                )
            # If key already present in DB, do update instead
            upsert = ins_stmt.on_conflict_do_update(
                    constraint='kv_unique_keycol_key',
                    set_=dict(valcol=rfm_s)
                    )

            try:
                connection.execute(upsert)
            except Exception as e:
                current_app.logger.error("Insert/Update failed on rfm edge ")
                current_app.logger.exception(e)
                return None

        return 0

    else :   # Malformed dict
        current_app.logger.error("Received rfm_edge dictionary with " + str(len(rfm_dict)) + " entries - expected 3")
        return None


def read_rfm_edges() :
    """Read the rfm_edge record from the DB and return the dict."""

    q = text("""SELECT valcol from kv_unique WHERE keycol = 'rfm_edges';""")

    with engine.begin() as connection:   # BEGIN TRANSACTION
        q_result = connection.execute(q)
        if q_result.rowcount == 0:
            current_app.logger.error("No rfm_edge entry found in DB")
            return None
        else:
            edge_string = q_result.fetchone()[0]
            try:
                edge_dict = json.loads(edge_string)   # Convert stored string to dict
            except json.decoder.JSONDecodeError:
                current_app.logger.error("rfm_edge entry found in DB was malformed")
                return None
                
            return edge_dict


#@admin_api.route("/api/admin/test_pd", methods=["GET"])  # enable to trigger externally
def pull_donations_for_rfm():
    """Pull donations records for RFM scoring.
       Returns a list of (matching_id:int , amount:float, close_date:string (yyyy-mm-dd))  tuples"""

    q = text("""select matching_id, amount, close_date
            FROM pdp_contacts
            JOIN salesforcedonations as sfd on pdp_contacts.source_id = sfd.contact_id
            where pdp_contacts.source_type = 'salesforcecontacts'
            ORDER BY matching_id; """)

    sfd_list = []

    with engine.connect() as connection:
        result = connection.execute(q)

        for row in result:
            sfd_list.append( (row[0], float(row[1]), str(row[2])) )

    #   return jsonify(sfd_list)  # enable if using endpoint, but it returns a lot of data
        return sfd_list


#@admin_api.route("/api/admin/test_pd", methods=["GET"])  # enable to trigger externally
def generate_dummy_rfm_scores():
    """For each matching_id, generate a random RFM score."""

    from random import choice
    from functools import partial 
    rc = partial( choice, range(1,6) )


    q = text("""select distinct matching_id from pdp_contacts
            ORDER BY matching_id; """)

    dummy_scores = []


    with engine.connect() as connection:
        result = connection.execute(q)

        for row in result:
            dummy_scores.append( ( row[0], str(rc()) +  str(rc()) + str(rc()) ) )  

    #   return jsonify(sfd_list)  # enable if using endpoint, but it returns a lot of data

    current_app.logger.debug("Inserting dummy scores...")
    count = insert_rfm_scores(dummy_scores)
    current_app.logger.debug("Finished inserting")


    return count




# Use this as a way to trigger functions for testing
# TODO: Remove when not needed
@admin_api.route("/api/admin/test_endpoint_gdrs", methods=["GET"])
def hit_gdrs():
    num_scores = generate_dummy_rfm_scores()
    return jsonify({"scores added" : num_scores})


# def pdfr():
#     dlist = pull_donations_for_rfm()
#     print("Returned " + str(len(dlist)) + " rows")
#     return jsonify( {'rows':len(dlist), 'row[0]': dlist[0]} )  # returns length and a sammple row


# def validate_rfm_edges():
#     d = read_rfm_edges()         # read out of DB
#     print("d is: \n" + str(d) )
#     write_rfm_edges(d)          # Write it back
#     d = read_rfm_edges()        # read it again     
#     print("round-trip d is : \n " + str(d) )
#     return "OK"

