from api.api import admin_api
import shutil
import os
from datetime import datetime
import json
from sqlalchemy.sql import text
from pipeline import flow_script
from config import engine
from flask import send_file, request, redirect, jsonify, current_app, abort
from api.file_uploader import validate_and_arrange_upload
from config import (
    RAW_DATA_PATH,
    OUTPUT_PATH,
    CURRENT_SOURCE_FILES_PATH,
    ZIPPED_FILES,
    LOGS_PATH,
)

ALLOWED_EXTENSIONS = {"csv", "xlsx"}


def __allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# file upload tutorial
@admin_api.route("/api/file", methods=["POST"])
def uploadCSV():
    current_app.logger.info("Uploading CSV")
    if "file" not in request.files:
        return jsonify({"error": "no file supplied"});

    for file in request.files.getlist("file"):
        if __allowed_file(file.filename):
            try:
                validate_and_arrange_upload(file, RAW_DATA_PATH)
            except Exception as e:
                current_app.logger.exception(e)
            finally:
                file.close()

    return jsonify({"success": "uploaded file"});


@admin_api.route("/api/files/<destination>", methods=["GET"])
def files(destination):
    current_app.logger.info("Start returning zip of all data")
    if request.args.get("download_current_btn"):
        source = RAW_DATA_PATH + destination
    if request.args.get("download_archived_btn"):
        source = RAW_DATA_PATH
    if request.args.get("download_output_btn"):
        source = OUTPUT_PATH

    zip_name = destination + "_data_out"

    try:
        current_app.logger.info(
            shutil.make_archive(ZIPPED_FILES + zip_name, "zip", source)
        )
        return send_file(
            ZIPPED_FILES + zip_name + ".zip",
            as_attachment=True,
            attachment_filename=zip_name + ".zip",
        )
    except Exception as e:
        return str(e)


@admin_api.route("/api/listCurrentFiles", methods=["GET"])
def list_current_files():
    result = None

    current_app.logger.info("Start returning file list")
    file_list_result = os.listdir(CURRENT_SOURCE_FILES_PATH)

    if len(file_list_result) > 0:
        result = file_list_result

    return jsonify(result)


@admin_api.route("/api/execute", methods=["GET"])
def execute():
    current_app.logger.info("Execute flow")
    flow_script.start_flow()

    current_time = datetime.now().ctime()
    statistics = get_statistics()

    last_execution_details = {"executionTime": current_time, "stats": statistics}

    last_execution_file = open(LOGS_PATH + "last_execution.json", "w")
    last_execution_file.write(json.dumps(last_execution_details))
    last_execution_file.close()

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
def list_statistics():
    try:
        last_execution_file = open(LOGS_PATH + "last_execution.json", "r")
        last_execution_details = json.loads(last_execution_file.read())
        last_execution_file.close()

    except (FileNotFoundError):
        current_app.logger.error("last_execution.json file was missing")
        return abort(500)

    except (json.JSONDecodeError):
        current_app.logger.error(
            "last_execution.json could not be decoded - possible corruption"
        )
        return abort(500)

    except Exception as e:
        current_app.logger.error("Failure reading last_execution.json: ", e)
        return abort(500)

    return jsonify(last_execution_details)


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
