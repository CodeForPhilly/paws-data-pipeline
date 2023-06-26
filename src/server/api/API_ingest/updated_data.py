
from sqlalchemy.orm import  sessionmaker
from simple_salesforce import Salesforce
from config import engine

import structlog
logger = structlog.get_logger()


def get_updated_contact_data():
    Session = sessionmaker(engine)

    qry = """ -- Collect latest foster/volunteer dates
        with ev_dates as 
        (select 
            person_id, 
            max(case when event_type=1 then time else null end) adopt,
            max(case when event_type=2 then time else null end) foster_out,
           --  max(case when event_type=3 then time else null end) rto,
            max(case when event_type=5 then time else null end) foster_return
           
        from 
            sl_animal_events sla
            left join sl_event_types sle on sle.id = sla.event_type
            
        where sle.id in (1,2,5)
        group by person_id
        order by person_id
        )
  

    select json_agg (upd)  as "cd" from (
            select
            slsf.source_id as "Contact_Record_Id__c" ,  -- long salesforce string
            slp.id   as  "Person_Id__c" ,           -- short PAWS-local shelterluv id
        
            --case
            --    when 
            --        (extract(epoch from now())::bigint - foster_out < 365*86400)  -- foster out in last year 
            --        or (extract(epoch from now())::bigint - foster_return < 365*86400) -- foster return 
            --    then 'Active'
            --    else 'Inactive'
            --end  as "Updated_Recent_Foster_Activity__c",
        
            foster_out as "Updated_Foster_Start_Date__c",
            foster_return as "Updated_Foster_End_Date__c",

            extract(epoch from min(vs.from_date)) as "Updated_First_Volunteer_Date__c",
            extract(epoch from max(vs.from_date)) as "Updated_Last_Volunteer_Date__c",
            sum(vs.hours) as "Updated_Total_Volunteer_Hours__c",
            vc.source_id::integer as   "Volgistics_Id__c" 
            
        from 
            ev_dates
            left join pdp_contacts slc on slc.source_id = person_id::text and slc.source_type = 'shelterluvpeople'
            left join pdp_contacts slsf on slsf.matching_id = slc.matching_id and slsf.source_type = 'salesforcecontacts'
            left join shelterluvpeople slp on slp.internal_id = person_id::text
            left join pdp_contacts vc on vc.matching_id = slc.matching_id and vc.source_type = 'volgistics'
            left join volgisticsshifts vs on vs.volg_id::text = vc.source_id 

    where 
        slsf.source_id is not null

        group by
            slsf.source_id,
            slp.id,
            vc.source_id,
            foster_out ,
            foster_return
        
    ) upd ;
    """

    with Session() as session:
        result = session.execute(qry)
        sfdata = result.fetchone()[0]
        logger.debug(sfdata)
        logger.debug("Query for Salesforce update returned %d records", len(sfdata))
        return sfdata