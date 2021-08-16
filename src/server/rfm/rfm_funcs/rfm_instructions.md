# RFM code run instructions

In order to obtain rfm scores a few dependencies will be required. 

1. The most up to date bin edges must be stored within the postgres database.
2. If bin edges must be updated use the following---via "src/server/api/admin_api.py"
    write_rfm_edges(rfm_dict : dict)

Once all above situations are satisfied create_scores can be run. 
create_scores.py is the main function which will output a list of tuples for matching_id and corresponding score.
This function requires a single input, query_date
    query_date should be pulled from the most recent data ingestion----once per week.

create_scores.py runs in 4 distinct steps
1. calculate recency since last donation over the total lifespan of data collection
2. calculate frequency over the past year from query date.
3. calculate monetary donations from the individual's max donation over the course of data lifespan.
4. concatenate recency, frequency, and monetary values into a single integer and pair these with individual matching ids to update via 'insert_rfm_scores'

