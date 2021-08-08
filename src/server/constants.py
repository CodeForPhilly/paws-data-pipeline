import os

# Determine if app is ran from docker or local by testing the env var "IS_LOCAL"
IS_LOCAL = os.getenv("IS_LOCAL")
BASE_PATH = "../local_files/" if IS_LOCAL == "True" else "/app/static/"


# Initiate local file system
RAW_DATA_PATH = BASE_PATH + "raw_data/"
OUTPUT_PATH = BASE_PATH + "output/"
LOGS_PATH = BASE_PATH + "logs/"
CURRENT_SOURCE_FILES_PATH = RAW_DATA_PATH + "current/"
REPORT_PATH = OUTPUT_PATH + "reports/"
ZIPPED_FILES = BASE_PATH + "zipped/"