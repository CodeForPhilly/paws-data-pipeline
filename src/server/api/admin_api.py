from api.api import admin_api
import os
from datetime import datetime
import json
from sqlalchemy.sql import text

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, exc, select
from pipeline import flow_script
from config import engine
from flask import request, redirect, jsonify, current_app, abort
from api.file_uploader import validate_and_arrange_upload

from api import jwt_ops
from config import (
    RAW_DATA_PATH,
    CURRENT_SOURCE_FILES_PATH,
)

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
                validate_and_arrange_upload(file, RAW_DATA_PATH)
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
    file_list_result = os.listdir(CURRENT_SOURCE_FILES_PATH)

    if len(file_list_result) > 0:
        result = file_list_result

    return jsonify(result)


@admin_api.route("/api/execute", methods=["GET"])
@jwt_ops.admin_required
def execute():
    current_app.logger.info("Execute flow")
    flow_script.start_flow()

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

    return jsonify(success=True)


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
                last_execution_details  = result.fetchone()[0]

        except Exception as e:
            current_app.logger.error("Failure reading Last Execution stats from DB - OK on first run")
        # Will happen on first run, shouldn't after 

    return last_execution_details


@admin_api.route("/api/get_execution_status/<int:job_id>", methods=["GET"])
@jwt_ops.admin_required
def get_exec_status(job_id):
    """ Get the execution status record from the DB for the specified job_id """


    engine.dispose() # we don't want other process's conn pool

    with engine.connect() as connection:

        s_jobid = 'job-' + str(job_id)        
        s = text("select valcol from kv_unique where keycol = :j ;")
        s = s.bindparams(j=s_jobid)
        result = connection.execute(s)
        if result.rowcount > 0:
            exec_status  = result.fetchone()[0]
        else:
            current_app.logger.warning("0 results for exec status query")
            exec_status = '{}'

    return exec_status




"""
@admin_api.route('/api/status', methods=['GET'])
def checkStatus():
    with engine.connect() as connection:
        query = text("SELECT now()")
        query_result = connection.execute(query)

        # Need to iterate over the results proxy
        results = {}
        for row in query_result:
            results = dict(row)
        return jsonify(results)
"""
