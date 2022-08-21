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

The values for the bins are calculated in `rfm_funcs/create_bins.py`,  which uses `https://pypi.org/project/jenkspy/` to split the R, F, and M data into quintiles. Recalculating the bins should be a fairly rare event, necessitated by a significant shift in donations. 

*Note: The code for this in master does not appear to be the latest. We need to find and merge that branch*

## Generating RFM scores





