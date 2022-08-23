# RFM Scoring  

## Bins

R,F, and M values range from 1-5. The bin ranges for these quintiles are stored in the database as a JSON string in the `kv_unique` table where the `keycol` value is 'rfm_edges'.  For example:

``` SQL
INSERT INTO "public"."kv_unique"("keycol","valcol") VALUES 
('rfm_edges',
    '{
        "r":{"5": 0, "4": 262, "3": 1097, "2": 1910, "1": 2851}, 
        "f": {"1": 0, "2": 1, "3": 2, "4": 3, "5": 4}, 
        "m": {"1": 0.0, "2": 50.0, "3": 75.0, "4": 100.0, "5": 210.0}
        }'
 ); 
 ```

The values for the bins are calculated in `rfm_funcs/create_bins.py`,  which uses `https://pypi.org/project/jenkspy/` to split the R, F, and M data into quintiles. Recalculating the bins should be a fairly rare event, necessitated by a significant shift in donations or focus.  Can we calculate a quality metric that might suggest when the bins should be recalculated?

Note: *The code for this in master may not be the latest. We need to find and merge that branch*

## Generating RFM scores

Refer to `server/rfm_funcs/create_scores.py`.

`create_scores()` loads donations data from the DB into a pandas dataframe.  
It then loads the rfm bin edges from the db into a dictionary `rfm_dict`.

### Recency  

`create_scores()` determines the last donation date of the set `max_close_date`, then builds the `days` array of the difference between the last donation date and the actual donation date.  

`gprouped_past_year` contains the days since last donation for each matching_id.   (Where is it limited to a year?)
The recency bins run in reverse, so the maximum days+1 value has to be appended to the recency bin to create the final bin edge for the oldest donation/lowest R score.
(What's happening with the 'cut')?

### Frequency  

### Monetary

$ amounts are binned and then the F+M scores are merged. (averaged?)

The R,F,M scores are combined and then written to the DB, linked to each donor by the matching_id.
