from datetime import datetime
import json
from sqlalchemy.sql import text
from flask import  current_app

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, exc, select

from config import db


metadata = MetaData()

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
    ex_stat = Table("execution_status", metadata, autoload=True, autoload_with=db.engine)

    """Log execution status (job_id, status, job_details) to DB """

    with db.engine.connect() as connection:
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
            current_app.logger.error("Insert/Update failed Execution status")
            current_app.logger.exception(e)


