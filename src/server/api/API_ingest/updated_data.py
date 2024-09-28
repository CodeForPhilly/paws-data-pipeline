
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
        sf.source_id as "contactId" ,  -- long salesforce string
        case 
        	when 
        		array_agg(sl.source_id) filter (where sl.source_id is not null) is null 
        	then '{}'::varchar[]
        	else array_agg(sl.source_id) filter (where sl.source_id is not null)   	
        end as "personIds",          -- short PAWS-local shelterluv id
        case
            when
                (extract(epoch from now())::bigint - (max(vol.last_date)/1000) < 365*86400)  -- volunteered in last year
            then 'Active'
            else 'Inactive'
        end  as "volunteerStatus",
        to_timestamp(max(foster_out) / 1000)::date  as "fosterStartDate",
        to_timestamp(max(foster_return) / 1000)::date  as "fosterEndDate",
        to_timestamp(min(vol.first_date) / 1000)::date "firstVolunteerDate",
        to_timestamp(max(vol.last_date) / 1000)::date "lastVolunteerDate",
        sum(vol.hours) as "totalVolunteerHours",
        case 
	        when 
	        	(array_agg(vc.source_id::integer) filter(where vc.source_id is not null)) is null 
	        then '{}'::int[] 
	        else array_agg(vc.source_id::integer) filter(where vc.source_id is not null) 
        end as "volgisticIds"
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
        group by sf.source_id
    ) upd;
    """

    with Session() as session:
        result = session.execute(qry)
        sfdata = result.fetchone()[0]
        if sfdata:
            logger.debug("Query for Salesforce update returned %d records", len(sfdata))
            return sfdata