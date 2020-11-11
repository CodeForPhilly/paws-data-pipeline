import os
import sqlalchemy as db
from sqlalchemy_utils import database_exists, create_database

# Determine if app is ran from docker or local by env var IS_LOCAL
BASE_PATH = '/app/static/'
POSTGRES_PASSWORD=os.getenv('POSTGRES_PASSWORD', 'thispasswordisverysecure')
POSTGRES_DATABASE=os.getenv('POSTGRES_DATABASE', 'paws')
POSTGRES_USER=os.getenv('POSTGRES_USER', 'postgres')
DB = 'postgresql://' + POSTGRES_USER + ':'+ POSTGRES_PASSWORD + '@paws-compose-db/' + POSTGRES_DATABASE

IS_LOCAL = os.getenv('IS_LOCAL', False)

if IS_LOCAL:
    BASE_PATH = '../local_files/'
    DB = os.getenv('LOCAL_DB_IP',
                   'postgresql://postgres:'+ POSTGRES_PASSWORD + '@localhost:5432/' + POSTGRES_DATABASE)

#best practices is to have only one engine per application process
#https://docs.sqlalchemy.org/en/13/core/connections.html
engine = db.create_engine(DB)

if not database_exists(engine.url):
    create_database(engine.url)

# print(database_exists(engine.url))

# Define global reusable paths
UPLOAD_PATH = BASE_PATH + 'uploads/'
OUTPUT_PATH = BASE_PATH + 'output/'
LOGS_PATH = BASE_PATH + 'logs/'
CURRENT_SOURCE_FILES_PATH = UPLOAD_PATH + 'current/'
REPORT_PATH = OUTPUT_PATH + 'reports/'
ZIPPED_FILES = BASE_PATH + 'zipped/'

if BASE_PATH != '/app/static/':
    try:
        os.mkdir(BASE_PATH)
        os.mkdir(UPLOAD_PATH)
        os.mkdir(OUTPUT_PATH)
        os.mkdir(LOGS_PATH)
        os.mkdir(CURRENT_SOURCE_FILES_PATH)
        os.mkdir(REPORT_PATH)
        os.mkdir(ZIPPED_FILES)
    except FileExistsError as e:
        print(e)
