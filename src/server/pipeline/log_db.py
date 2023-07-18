from datetime import datetime
import json
from sqlalchemy.sql import text
from flask import  current_app
import time

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, exc, select

from config import engine
import structlog
logger = structlog.get_logger()

metadata = MetaData()

ex_stat = Table("execution_status", metadata, autoload=True, autoload_with=engine)
kvt = Table("kv_unique", metadata, autoload=True, autoload_with=engine)


# Alembic version bfb1262d3195

# CREATE TABLE public.execution_status (
# 	"_id" serial NOT NULL,
# 	job_id int4 NOT NULL,
# 	stage varchar(32) NOT NULL,
# 	status varchar(32) NOT NULL,
# 	details varchar(128) NOT NULL,
# 	update_stamp timestamp NOT NULL DEFAULT now(),
# 	CONSTRAINT execution_status_pkey null
# );



def log_exec_status(job_id: str, exec_stage: str, exec_status: str, job_details: str):
    """Log execution status (job_id, status, job_details) to DB """

    with engine.connect() as connection:
        ins_stmt = insert(ex_stat).values(               # Postgres-specific insert() supporting ON CONFLICT 
            job_id =  job_id,
            stage = exec_stage, 
            status = exec_status,
            details = json.dumps(job_details)
            )

        # If key already present in DB, do update instead 
        upsert = ins_stmt.on_conflict_do_update(
                constraint='uq_job_id',
                set_=dict( stage = exec_stage, status = exec_status,  details = json.dumps(job_details))
                )

        try:
            connection.execute(upsert)
        except Exception as e:
            logger.error("Insert/Update failed,  Execution status")
            logger.error(e)


def log_volgistics_update():
    """Log Volgistics data update"""

    timestamp = datetime.now().ctime()

    with engine.connect() as connection:
        ins_stmt = insert(kvt).values(               
            keycol = 'last_volgistics_update',
            valcol = timestamp,
            )
        # If key already present in DB, do update instead
        upsert = ins_stmt.on_conflict_do_update(
                constraint='kv_unique_keycol_key',
                set_=dict(valcol=timestamp)
                )

        try:
            connection.execute(upsert)
        except Exception as e:
            logger.error("Insert/Update failed on Volgistics stats")
            logger.error(e)


def log_shelterluv_update():
    """Log Shelterluv data update"""

    timestamp =  datetime.now().ctime()

    with engine.connect() as connection:
        ins_stmt = insert(kvt).values(               
            keycol = 'last_shelterluv_update',
            valcol = timestamp,
            )
        # If key already present in DB, do update instead
        upsert = ins_stmt.on_conflict_do_update(
                constraint='kv_unique_keycol_key',
                set_=dict(valcol=timestamp)
                )

        try:
            connection.execute(upsert)
        except Exception as e:
            logger.error("Insert/Update failed on Shelterluv stats")
            logger.error(e)


def log_salesforce_update():
    """Log SalesForce data update"""

    timestamp = datetime.now().ctime()

    with engine.connect() as connection:
        ins_stmt = insert(kvt).values(               
            keycol = 'last_salesforce_update',
            valcol = timestamp,
            )
        # If key already present in DB, do update instead
        upsert = ins_stmt.on_conflict_do_update(
                constraint='kv_unique_keycol_key',
                set_=dict(valcol=timestamp)
                )

        try:
            connection.execute(upsert)
        except Exception as e:
            logger.error("Insert/Update failed on SalseForce stats")
            logger.error(e)
