import pandas as pd
from config import engine
from donations_importer import validate_import_sfd
from flask import current_app
from models import ManualMatches, SalesForceContacts, ShelterluvPeople, Volgistics
from shifts_importer import validate_import_vs
from werkzeug.utils import secure_filename

import structlog
logger = structlog.get_logger()

SUCCESS_MSG = "Uploaded Successfully!"


def validate_and_arrange_upload(file):
    logger.info("Start uploading file: " + file.filename)
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
        logger.debug("File extension is CSV")
        df = pd.read_csv(file, dtype="string")

        if {"salesforcecontacts", "volgistics", "shelterluvpeople"}.issubset(df.columns):
            logger.debug("File appears to be salesforcecontacts, volgistics, or shelterluvpeople (manual)")
            ManualMatches.insert_from_df(df, conn)
            return
        elif {"Animal_ids", "Internal-ID"}.issubset(df.columns):
            logger.debug("File appears to be shelterluvpeople")
            ShelterluvPeople.insert_from_df(df, conn)
            return

    if file_extension == "xlsx":
        excel_file = pd.ExcelFile(file)
        if {"Master", "Service"}.issubset(excel_file.sheet_names):
            logger.debug("File appears to be Volgistics")
            # Volgistics
            validate_import_vs(file, conn)
            Volgistics.insert_from_file(excel_file, conn)
            return

        df = pd.read_excel(excel_file)
        if "Contact ID 18" in df.columns:
            # Salesforce something-or-other
            if "Amount" in df.columns:
                # Salesforce donations
                logger.debug("File appears to be Salesforce donations")
                validate_import_sfd(file, conn)
                return
            else:
                # Salesforce contacts
                logger.debug("File appears to be Salesforce contacts")
                SalesForceContacts.insert_from_file_df(df, conn)
                return

    logger.error("Don't know how to process file: %s",  file.filename)