import pandas as pd
from config import engine
from donations_importer import validate_import_sfd
from flask import current_app
from models import ManualMatches, SalesForceContacts, ShelterluvPeople, Volgistics
from shifts_importer import validate_import_vs
from werkzeug.utils import secure_filename

SUCCESS_MSG = "Uploaded Successfully!"


def validate_and_arrange_upload(file):
    current_app.logger.info("Start uploading file: " + file.filename)
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
        df = pd.read_csv(file, dtype="string")

        if {"salesforcecontacts", "volgistics", "shelterluvpeople"}.issubset(df.columns):
            ManualMatches.insert_from_df(df, conn)
            return
        elif {"Animal_ids", "Internal-ID"}.issubset(df.columns):
            ShelterluvPeople.insert_from_df(df, conn)
            return

    if file_extension == "xlsx":
        excel_file = pd.ExcelFile(file)
        if {"Master", "Service"}.issubset(excel_file.sheet_names):
            # Volgistics
            validate_import_vs(file, conn)
            Volgistics.insert_from_file(excel_file, conn)
            return

        df = pd.read_excel(excel_file)
        if "Contact ID 18" in df.columns:
            # Salesforce something-or-other
            if "Amount" in df.columns:
                # Salesforce donations
                validate_import_sfd(file, conn)
                return
            else:
                # Salesforce contacts
                SalesForceContacts.insert_from_file_df(df, conn)
                return

    current_app.logger.error(f"Don't know how to process file {file.filename}")