import time
import traceback

from api import admin_api
from config import engine
from flask import current_app
from models import (
    ManualMatches,
    PdpContacts,
    SalesForceContacts,
    ShelterluvPeople,
    Volgistics,
)
from networkx import Graph, connected_components
from sqlalchemy import (
    Column,
    Integer,
    MetaData,
    Table,
    and_,
    delete,
    func,
    insert,
    or_,
    select,
    text,
    update,
)

from pipeline import log_db
import structlog
logger = structlog.get_logger()

def start_flow():
    start = time.time()
    job_id = admin_api.start_job()
    job_outcome = None
    trace_back_string = None

    if not job_id:
        logger.info("Failed to get job_id")
        return "busy"

    try:
        log_db.log_exec_status(job_id, "start_flow", "executing", "")

        with engine.begin() as conn:
            # Here's how we match:
            # 1. Clear pdp_contacts (the old matches).
            # 2. Go through each raw data source table (e.g. salesforcecontacts,
            #    volgistics) and copy the latest data for each contact into
            #    pdp_contacts.
            # 3. Execute a join of pdp_contacts to itself using names, emails,
            #    phone numbers, etc. to get a list of pairs of pdp_contacts ids
            #    that "match."
            # 4. Join manual_matches to pdp_contacts to get the pdp_contacts ids
            #    of our manual matches.
            #
            # Steps 3 and 4 both produce lists of pairs of ids. Next we need to
            # associate an id with each group of matches. Note that if A matches
            # B and B matches C, then A and C should get the same match id. We
            # can thus think of "matches" as edges in a graph of id vertices,
            # and match groups as connected components in that graph. So:
            #
            # 5. Load all the matches into a Graph() and compute its connected
            #    components.
            # 6. Update each row in pdp_contacts to give it a match id
            #    corresponding to its connected componenet.

            logger.debug("Clearing pdp_contacts to prepare for match")
            reset_pdp_contacts_with_unmatched(conn)

            logger.debug("Removing invalid entries from pdp_contacts")
            filter_invalid_pdp_data(conn)

            logger.debug("Computing automatic matches")
            automatic_matches = get_automatic_matches(conn)
            logger.debug("Computing manual matches")
            manual_matches = get_manual_matches(conn)

            match_graph = Graph()
            logger.debug("Adding automatic matches to graph")
            match_graph.add_edges_from(automatic_matches)
            logger.debug("Adding manual matches to graph")
            match_graph.add_edges_from(manual_matches)
            logger.debug("Processing graph")
            match_groups = connected_components(match_graph)

            logger.debug("Updating pdp_contacts with match ids")
            update_matching_ids(match_groups, conn)

            logger.debug("Finished flow script run")
            job_outcome = "completed"
            log_db.log_exec_status(job_id, "flow", "complete", "")

    except Exception as e:
        logger.error(e)
        trace_back_string = traceback.format_exc()
        logger.error(trace_back_string)

    finally:
        if job_outcome != "completed":

            log_db.log_exec_status(job_id, "flow", "error", trace_back_string)
            logger.error(
                "Uncaught error status, setting job status to 'error' "
            )
            job_outcome = "error"
            return "error"

    logger.info(
        "Pipeline execution took %s seconds ", format(time.time() - start)
    )
    return job_outcome


def reset_pdp_contacts_with_unmatched(conn):
    conn.execute(delete(PdpContacts))
    conn.execute(SalesForceContacts.insert_into_pdp_contacts())
    conn.execute(Volgistics.insert_into_pdp_contacts())
    conn.execute(ShelterluvPeople.insert_into_pdp_contacts())


def name_to_array(n):
    delims = text("'( and | & |, | )'")
    return func.regexp_split_to_array(
        func.lower(func.translate(n, text("'\"'"), text("''"))), delims
    )


def compare_names(n1, n2):
    return name_to_array(n1).bool_op("&&")(name_to_array(n2))


def filter_invalid_pdp_data(conn):
    pc = PdpContacts.__table__.alias()
    lower_first_name = func.lower(pc.c.first_name)
    lower_last_name = func.lower(pc.c.last_name)

    unknown = and_(
        lower_first_name.ilike("%unknown%"),
        lower_last_name.ilike("%unknown%")
    )

    question_mark = and_(
        lower_first_name == '?',
        lower_last_name == '?'
    )

    john_or_jane_doe = and_(
        or_(
            lower_first_name == "john",
            lower_first_name == "jane"
        ),
        lower_last_name == "doe"
    )

    no_name = and_(
        lower_first_name == "no",
        lower_last_name == "name"
    )

    none_friends = and_(
        lower_first_name.is_(None),
        lower_last_name == "friends"
    )

    red_flag = or_(
        lower_first_name == "(red flag)",
        lower_last_name == "(red flag)"
    )

    # It would be preferable for the following two conditions to use sqlalchemy statements,
    # but it proved surprisingly difficult to convert sqlalchemy regexp results into booleans
    digits_only = and_(
        text("""LOWER(first_name) ~ '^\d+$'"""),
        text("""LOWER(last_name) ~ '^\d+$'""")
    )
    no_name_no_name = and_(
        text("""LOWER(first_name) ~ 'no\s?name'"""),
        text("""LOWER(last_name) ~ 'no\s?name'""")
    )

    composite_condition = or_(
        unknown,
        question_mark,
        john_or_jane_doe,
        no_name,
        none_friends,
        red_flag,
        digits_only,
        no_name_no_name,
    )

    delete_stmt = delete(pc).where(composite_condition)

    return conn.execute(delete_stmt)


def get_automatic_matches(conn):
    pc1 = PdpContacts.__table__.alias()
    pc2 = PdpContacts.__table__.alias()
    match_stmt = select(pc1.c._id, pc2.c._id).join(
        pc2,
        and_(
            or_(
                and_(
                    compare_names(pc1.c.first_name, pc2.c.first_name),
                    compare_names(pc1.c.last_name, pc2.c.last_name),
                ),
                and_(
                    compare_names(pc1.c.first_name, pc2.c.last_name),
                    compare_names(pc1.c.last_name, pc2.c.first_name),
                ),
            ),
            or_(
                func.lower(pc1.c.email) == func.lower(pc2.c.email),
                pc1.c.mobile == pc2.c.mobile,
            ),
            # This ensures we don't get e.g. every row matching itself
            pc1.c._id < pc2.c._id,
        ),
    )
    return conn.execute(match_stmt)


def get_manual_matches(conn):
    pc1 = PdpContacts.__table__.alias()
    pc2 = PdpContacts.__table__.alias()
    stmt = (
        select(pc1.c._id, pc2.c._id)
        .select_from(ManualMatches)
        .join(
            pc1,
            (ManualMatches.source_type_1 == pc1.c.source_type)
            & (ManualMatches.source_id_1 == pc1.c.source_id),
        )
        .join(
            pc2,
            (ManualMatches.source_type_2 == pc2.c.source_type)
            & (ManualMatches.source_id_2 == pc2.c.source_id),
        )
    )
    return conn.execute(stmt)


def update_matching_ids(match_groups, conn):
    # match_groups doesn't include singletons, but we should still each
    # unmatched record gets a sane matching_id (that is, its own id)
    matching_ids_by_id = {id: id for (id,) in conn.execute(select(PdpContacts._id))}
    for match_group in match_groups:
        matching_id = min(match_group)
        for id in match_group:
            matching_ids_by_id[id] = matching_id

    # Load all the new id/matching-id pairs into a temp table so that we can do
    # a fast UPDATE FROM to set all the matching ids in pdp_contacts
    temp_table = Table(
        "_tmp_matching_id_update",
        MetaData(),  # this is a temp table, we don't want to affect our knowledge of "real" tables
        Column("_id", Integer, primary_key=True),
        Column("matching_id", Integer),
        prefixes=["TEMPORARY"],
        postgresql_on_commit="DROP",
    )
    temp_table.create(conn)
    conn.execute(
        insert(temp_table),
        [
            {"_id": _id, "matching_id": matching_id}
            for (_id, matching_id) in matching_ids_by_id.items()
        ],
    )
    conn.execute(
        update(PdpContacts)
        .where(PdpContacts._id == temp_table.c._id)
        .values(matching_id=temp_table.c.matching_id)
    )
