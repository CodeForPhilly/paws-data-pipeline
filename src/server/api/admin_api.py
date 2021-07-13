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
from api.API_ingest import ingest_sources_from_api

from api import jwt_ops
from config import CURRENT_SOURCE_FILES_PATH

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


@admin_api.route("/api/ingestRawData", methods=["GET"])
def ingest_raw_data():
    try:
        ingest_sources_from_api.start()
    except Exception as e:
        current_app.logger.exception(e)

    return jsonify({'outcome': 'OK'}), 200


@admin_api.route("/api/listCurrentFiles", methods=["GET"])
@jwt_ops.admin_required
def list_current_files():
    result = None

    current_app.logger.info("Start returning file list")
    file_list_result = os.listdir(CURRENT_SOURCE_FILES_PATH)

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




# """
# @admin_api.route('/api/status', methods=['GET'])
# def checkStatus():
#     with engine.connect() as connection:
#         query = text("SELECT now()")
#         query_result = connection.execute(query)

#         # Need to iterate over the results proxy
#         results = {}
#         for row in query_result:
#             results = dict(row)
#         return jsonify(results)
# """
