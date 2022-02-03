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
    update,
)

from pipeline import log_db


def start_flow():
    start = time.time()
    job_id = admin_api.start_job()
    job_outcome = None
    trace_back_string = None

    if not job_id:
        current_app.logger.info("Failed to get job_id")
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
            

            current_app.logger.info("Clearing pdp_contacts to prepare for match")
            reset_pdp_contacts_with_unmatched(conn)

            current_app.logger.info("Computing matches")
            automatic_matches = get_automatic_matches(conn)
            manual_matches = get_manual_matches(conn)

            match_graph = Graph()
            match_graph.add_edges_from(automatic_matches)
            match_graph.add_edges_from(manual_matches)
            match_groups = connected_components(match_graph)

            current_app.logger.info("Updating pdp_contacts with match ids")
            update_matching_ids(match_groups, conn)

            current_app.logger.info("Finished flow script run")
            job_outcome = "completed"
            log_db.log_exec_status(job_id, "flow", "complete", "")

    except Exception as e:
        current_app.logger.error(e)
        trace_back_string = traceback.format_exc()
        current_app.logger.error(trace_back_string)

    finally:
        if job_outcome != "completed":

            log_db.log_exec_status(job_id, "flow", "error", trace_back_string)
            current_app.logger.error(
                "Uncaught error status, setting job status to 'error' "
            )
            job_outcome = "error"
            return "error"

    current_app.logger.info(
        "Pipeline execution took {} seconds ".format(time.time() - start)
    )
    return job_outcome


def reset_pdp_contacts_with_unmatched(conn):
    conn.execute(delete(PdpContacts))
    conn.execute(SalesForceContacts.insert_into_pdp_contacts())
    conn.execute(Volgistics.insert_into_pdp_contacts())
    conn.execute(ShelterluvPeople.insert_into_pdp_contacts())


def get_automatic_matches(conn):
    pc1 = PdpContacts.__table__.alias()
    pc2 = PdpContacts.__table__.alias()
    match_stmt = select(pc1.c._id, pc2.c._id).join(
        pc2,
        and_(
            or_(
                and_(
                    func.lower(pc1.c.first_name) == func.lower(pc2.c.first_name),
                    func.lower(pc1.c.last_name) == func.lower(pc2.c.last_name),
                ),
                and_(
                    func.lower(pc1.c.first_name) == func.lower(pc2.c.last_name),
                    func.lower(pc1.c.last_name) == func.lower(pc2.c.first_name),
                ),
            ),
            or_(
                pc1.c.email == pc2.c.email,
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
