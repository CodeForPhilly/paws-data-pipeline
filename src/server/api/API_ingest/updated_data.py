
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
        sf.source_id as "Id" ,  -- long salesforce string
        sle.person_id   as  "Person_Id__c",           -- short PAWS-local shelterluv id
        case
            when
                (extract(epoch from now())::bigint - foster_out < 365*86400)  -- foster out in last year
                or (extract(epoch from now())::bigint - foster_return < 365*86400) -- foster return
            then 'Active'
            else 'Inactive'
        end  as "Foster_Activity__c",
        foster_out as "Foster_Start_Date__c",
        foster_return as "Foster_End_Date__c",
        vol.first_date "First_volunteer_date__c",
        vol.last_date "Last_volunteer_date__c",
        vol.hours as "Total_volunteer_hours__c",
        vc.source_id::integer as   "Volgistics_Id__c"
        from (
            select source_id, matching_id from pdp_contacts sf
            where sf.source_type = 'salesforcecontacts'
        ) sf
        left join pdp_contacts sl on sl.matching_id = sf.matching_id and sl.source_type = 'shelterluvpeople'
        left join (
            select
            person_id,
            max(case when event_type=1 then time else null end) * 1000 adopt,
            max(case when event_type=2 then time else null end) * 1000 foster_out,
            --  max(case when event_type=3 then time else null end) rto,
            max(case when event_type=5 then time else null end) * 1000 foster_return
            from sl_animal_events
            group by person_id
        ) sle on sle.person_id::text = sl.source_id
        left join pdp_contacts vc on vc.matching_id = sf.matching_id and vc.source_type = 'volgistics'
        left join (
            select
            volg_id,
            sum(hours) as hours,
            extract(epoch from min(from_date)) * 1000 as first_date,
            extract(epoch from max(from_date)) * 1000 as last_date
            from volgisticsshifts
            group by volg_id
        ) vol on vol.volg_id::text = vc.source_id
        where sl.matching_id is not null or vc.matching_id is not null
    ) upd;
    """

    with Session() as session:
        result = session.execute(qry)
        sfdata = result.fetchone()[0]
        logger.debug(sfdata)
        logger.debug("Query for Salesforce update returned %d records", len(sfdata))
        return sfdata