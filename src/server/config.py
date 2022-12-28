import os
import sys
import sqlalchemy as db
import models
from constants import IS_LOCAL, BASE_PATH, RAW_DATA_PATH, OUTPUT_PATH, LOGS_PATH, REPORT_PATH, ZIPPED_FILES

import logging
import structlog
from structlog.processors import CallsiteParameter


# structlog setup for complete app

# Formatters
shared_processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.processors.TimeStamper(fmt="iso", utc=True ),
        structlog.processors.CallsiteParameterAdder(
            [
                CallsiteParameter.FILENAME,
                CallsiteParameter.FUNC_NAME,
                CallsiteParameter.LINENO,
            ])
        ]

# Select output processor depending if running locally/interactively or not
if sys.stderr.isatty():   # Pretty-print
        processors = shared_processors + [structlog.dev.ConsoleRenderer(), ]
else:   # Emit structured/JSON
        processors = shared_processors +  [ structlog.processors.dict_tracebacks, structlog.processors.JSONRenderer(), ]

structlog.configure(
    processors=processors, 
    wrapper_class=structlog.make_filtering_bound_logger(logging.NOTSET),
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
    cache_logger_on_first_use=False
)
logger = structlog.get_logger()


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

# Run Alembic to create managed tables
# from alembic.config import Config
# from alembic import command

# alembic_cfg = Config("alembic.ini")
# command.stamp(alembic_cfg, "head")

# logger.warn("Testing")

with engine.connect() as connection:
    import db_setup.base_users
    db_setup.base_users.create_base_roles()  # IFF there are no roles already
    db_setup.base_users.create_base_users()  # IFF there are no users already
    db_setup.base_users.populate_sl_event_types()  # IFF there are no event types already
    db_setup.base_users.populate_rfm_mapping_table()   # Set to True to force loading latest version of populate script
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
