def donations_rfm(csv, query_date):
    '''This script will take csv files and create RFM scores for all PAWS donations
    csv = path to csv file as string
    query_date = date data was queried
    '''

    import pandas as pd
    import numpy as np
    import jenkspy
    from datetime import datetime, date



    ####
    # read in csv
    donations = pd.read_csv('csv')

    donations['Close_Date'] =pd.to_datetime(donations_2021['Close_Date']).dt.date

    ##################################################################################
    # Calculate recency score
    from recency_score import recency_score
    grouped_df, recency_bins, quantile_scores= recency_score(donations_df, query_date)

    ###################################################################################
    # Calculate frequency scores

    
