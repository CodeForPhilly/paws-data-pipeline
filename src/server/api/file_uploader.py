from config import engine
from donations_importer import validate_import_sfd
from flask import current_app
from models import ManualMatches, SalesForceContacts, ShelterluvPeople, Volgistics
from pipeline.log_db import log_volgistics_update
from volgistics_importer import open_volgistics, validate_import_vs, volgistics_people_import
from werkzeug.utils import secure_filename
import structlog
logger = structlog.get_logger()

SUCCESS_MSG = "Uploaded Successfully!"


def validate_and_arrange_upload(file):
    logger.info("Start uploading file: %s  ", file.filename)
    filename = secure_filename(file.filename)
    file_extension = filename.rpartition(".")[2]
    with engine.begin() as conn:
        determine_upload_type(file, file_extension, conn)


def determine_upload_type(file, file_extension, conn):
    # Yes, this method of discovering what kind of file we have by looking at
    # the extension and columns is silly. We'd like to get more of our data from
    # automatically pulling from vendor APIs directly, in which case we'd know
    # what kind of data we had.
    if file_extension == "csv":
        logger.warn("%s: We no longer support CSV files", file.filename)
        return

    if file_extension == "xlsx":
        # Assume it's Volgistics
        workbook = open_volgistics(file)
        if workbook:
            validate_import_vs(workbook)
            volgistics_people_import(workbook)
            workbook.close()
            log_volgistics_update()
        return

    logger.error("Don't know how to process file: %s",  file.filename)