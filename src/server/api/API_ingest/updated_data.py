
import structlog
from sqlalchemy.orm import sessionmaker

from config import engine

logger = structlog.get_logger()


def get_updated_contact_data():
    Session = sessionmaker(engine)

    qry = """ -- Collect latest foster/volunteer dates
    select json_agg (upd)  as "cd"
    from (
        select 
        salesforce.source_id as "contactId",
        shelterluv.person_ids as "personIds",
        case
            when volgistics.last_shift_date > now() - interval '1 year' then 'Active' else 'InActive'
        end as "volunteerStatus",
        shelterluv.foster_start as "fosterStartDate",
        shelterluv.foster_end as "fosterEndDate",
        volgistics.first_volunteer_date as "firstVolunteerDate",
        volgistics.last_shift_date as "lastShiftDate",
        volgistics.total_hours as "totalVolunteerHours",
        volgistics.volg_ids as "volgisticIds"
        from (
            select * from pdp_contacts pc where source_type = 'salesforcecontacts'
        ) salesforce
        left join (
            select matching_id, array_agg(distinct v."number"::int) volg_ids, sum(hours) total_hours, 
            min(from_date) first_volunteer_date, max(from_date) last_shift_date 
            from volgistics v
            left join volgisticsshifts v2 on v2.volg_id::varchar = v.number
            inner join pdp_contacts pc on pc.source_id = v2.volg_id::varchar and pc.source_type = 'volgistics'
            group by matching_id
        ) volgistics on volgistics.matching_id = salesforce.matching_id
        left join (
            select
            matching_id, array_agg(distinct p.internal_id) as person_ids,
            max(case when event_type=1 then to_timestamp(time) else null end) adopt,
            min(case when event_type=2 then to_timestamp(time) else null end) foster_start,
            max(case when event_type=5 then to_timestamp(time) else null end) foster_end
            from shelterluvpeople p
            left join sl_animal_events sae on sae.person_id::varchar = p.internal_id
            inner join pdp_contacts pc on pc.source_id = p.internal_id
            group by matching_id
        ) shelterluv on shelterluv.matching_id = salesforce.matching_id
        where volgistics.matching_id is not null or shelterluv.matching_id is not null
    ) upd;
    """

    with Session() as session:
        result = session.execute(qry)
        sfdata = result.fetchone()[0]
        if sfdata:
            logger.debug("Query for Salesforce update returned %d records", len(sfdata))
            return sfdata