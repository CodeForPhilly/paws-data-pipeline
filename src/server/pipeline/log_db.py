from datetime import datetime
import json
from sqlalchemy.sql import text
from flask import  current_app

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, exc, select

from config import engine


metadata = MetaData()

kvt = Table("kv_unique", metadata, autoload=True, autoload_with=engine)



def log_exec_status(job_id: str, job_status: dict):

    # Write Last Execution stats to DB  
    # See Alembic Revision ID: 05e0693f8cbb for table definition
    with engine.connect() as connection:
        ins_stmt = insert(kvt).values(               # Postgres-specific insert() supporting ON CONFLICT 
            keycol = 'job-' + job_id,
            valcol = json.dumps(job_status)
            )

        # If key already present in DB, do update instead 
        upsert = ins_stmt.on_conflict_do_update(
                constraint='kv_unique_keycol_key',
                set_=dict(valcol=json.dumps(job_status))
                )

        try:
            connection.execute(upsert)
        except Exception as e:
            current_app.logger.error("Insert/Update failed Execution status")
            current_app.logger.exception(e)


