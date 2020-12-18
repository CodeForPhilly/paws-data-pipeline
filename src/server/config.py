import os
import sqlalchemy as db
from sqlalchemy_utils import database_exists, create_database

import models


# from user_mgmt import base_users


# Determine if app is ran from docker or local by testing the env var "IS_LOCAL"
IS_LOCAL = os.getenv("IS_LOCAL")
BASE_PATH = "../local_files/" if IS_LOCAL == "True" else "/app/static/"

# Initiate postgres DB
# best practices is to have only one engine per application process
# https://docs.sqlalchemy.org/en/13/core/connections.html
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "thispasswordisverysecure")
POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE", "paws")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")

if IS_LOCAL == "True":
    DB = os.getenv(
        "LOCAL_DB_IP",
        "postgresql://postgres:"
        + POSTGRES_PASSWORD
        + "@localhost:5432/"
        + POSTGRES_DATABASE,
    )
else:
    DB = (
        "postgresql://"
        + POSTGRES_USER
        + ":"
        + POSTGRES_PASSWORD
        + "@paws-compose-db/"
        + POSTGRES_DATABASE
    )

engine = db.create_engine(DB)

if not database_exists(engine.url):
    create_database(engine.url)
    with engine.connect() as connection:
        models.Base.metadata.create_all(connection)


with engine.connect() as connection:
    import user_mgmt.base_users

    user_mgmt.base_users.create_base_users()


# Initiate local file system
RAW_DATA_PATH = BASE_PATH + "raw_data/"
OUTPUT_PATH = BASE_PATH + "output/"
LOGS_PATH = BASE_PATH + "logs/"
CURRENT_SOURCE_FILES_PATH = RAW_DATA_PATH + "current/"
REPORT_PATH = OUTPUT_PATH + "reports/"
ZIPPED_FILES = BASE_PATH + "zipped/"

os.makedirs(BASE_PATH, exist_ok=True)
os.makedirs(RAW_DATA_PATH, exist_ok=True)
os.makedirs(OUTPUT_PATH, exist_ok=True)
os.makedirs(LOGS_PATH, exist_ok=True)
os.makedirs(CURRENT_SOURCE_FILES_PATH, exist_ok=True)
os.makedirs(REPORT_PATH, exist_ok=True)
os.makedirs(ZIPPED_FILES, exist_ok=True)

if not (os.path.exists(LOGS_PATH + "last_execution.json")):
    f = open(
        LOGS_PATH + "last_execution.json", "w"
    )  # Prevent 500 error from /api/statistics
    f.write("{}")
    f.close()
