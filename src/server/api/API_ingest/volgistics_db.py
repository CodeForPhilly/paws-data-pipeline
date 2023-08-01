from sqlalchemy import Table, MetaData
from sqlalchemy.orm import sessionmaker

from config import engine

import structlog
logger = structlog.get_logger()

def insert_volgistics_people(row_list):

    row_count = 0
    try:
        Session = sessionmaker(engine)
        session = Session()
        metadata = MetaData()
        volg_table = Table("volgistics", metadata, autoload=True, autoload_with=engine)

        result = session.execute("TRUNCATE table volgistics;")
        ret = session.execute(volg_table.insert(row_list))

        row_count = ret.rowcount

        session.commit()  # Commit all inserted rows
        session.close()
    except Exception as e:
        row_count = 0
        logger.error("Exception inserting volgistics people")
        logger.exception(e)
    return row_count


def insert_volgistics_shifts(row_list):

    row_count = 0
    try:
        Session = sessionmaker(engine)
        session = Session()
        metadata = MetaData()
        volg_table = Table("volgisticsshifts", metadata, autoload=True, autoload_with=engine)

        result = session.execute("TRUNCATE table volgisticsshifts;")
        ret = session.execute(volg_table.insert(row_list))

        row_count = ret.rowcount

        session.commit()  # Commit all inserted rows
        session.close()
    except Exception as e:
        row_count = 0
        logger.error("Exception inserting volgistics shifts")
        logger.exception(e.pgerror)
    return row_count
