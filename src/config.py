import os

# Determine if app is ran from docker or local by env var IS_LOCAL
BASE_PATH = '/app/static/'
DB = 'postgresql://postgres:thispasswordisverysecure@paws-compose-db/postgres'

IS_LOCAL = os.getenv('IS_LOCAL', False)

if IS_LOCAL:
    BASE_PATH = '../local_files/'
    DB = os.getenv('LOCAL_DB_IP',
                   'postgresql://postgres:thispasswordisverysecure@localhost:5432/postgres')



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
    except FileExistsError:
        print("One or more Directories already exist")


