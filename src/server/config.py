import os
import models
from constants import IS_LOCAL, BASE_PATH, RAW_DATA_PATH, OUTPUT_PATH, LOGS_PATH, REPORT_PATH, ZIPPED_FILES
from flask_sqlalchemy import SQLAlchemy


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

db = SQLAlchemy()

# Run Alembic to create managed tables
# from alembic.config import Config
# from alembic import command

# alembic_cfg = Config("alembic.ini")
# command.stamp(alembic_cfg, "head")

# with db.connect() as connection:
#     import user_mgmt.base_users
#     user_mgmt.base_users.create_base_roles()  # IFF there are no roles already
#     user_mgmt.base_users.create_base_users()  # IFF there are no users already
#     user_mgmt.base_users.populate_rfm_mapping_table()   # Set to True to force loading latest version of populate script
                                                                       # found in the server/alembic directory

# Create these directories only one time - when initializing
if not os.path.isdir(BASE_PATH):
    os.makedirs(BASE_PATH, exist_ok=True)
    os.makedirs(RAW_DATA_PATH, exist_ok=True)
    os.makedirs(OUTPUT_PATH, exist_ok=True)
    os.makedirs(LOGS_PATH, exist_ok=True)
    os.makedirs(RAW_DATA_PATH, exist_ok=True)
    os.makedirs(REPORT_PATH, exist_ok=True)
    os.makedirs(ZIPPED_FILES, exist_ok=True)
