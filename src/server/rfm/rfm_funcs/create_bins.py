def create_bins(data, query_date):
    '''This script will take table data and bin edges for RFM scores for all PAWS donations

    query_date = date data was queried
    '''

    import pandas as pd
    import numpy as np
    import jenkspy
    from datetime import datetime, date
    import os



    ####
    # read in data from database as list of tuples
    df = pull_donations_for_rfm()
    df = pd.DataFrame(df, columns=['matching_id', 'amount', 'close_date'])

    donations_df['Close_Date'] =pd.to_datetime(df['Close_Date']).dt.date

    ##################################################################################
    # Calculate recency bins
    from recency_bins import recency_bins
    recency_bins, quantile_scores= recency_bins(donations_df, query_date)

    ###################################################################################
    # Calculate frequency bins
    from frequency_bins import frequency_bins

    jenks_frequency_bins, human_frequency_bins = frequency_bins(donations_df)


        def checkIfDuplicates(listOfElems):
        ''' Check if given list contains any duplicates '''
        for elem in listOfElems:
            if listOfElems.count(elem) > 1:
                return True
        return False

        duplicats_bool = checkIfDuplicates(jenks_frequency_bins)
        if duplicates_bool  == True:
            final_frequency_bins = human_frequency_bins

    ###################################################################################
    # Calculate Amount bins
    from amount_bins import amount_bins

    amount_jenks_bins, human_amount_bins = amount_bins(donations_df)



    ###################################################################################
    # Write bins to dict
    bins_dict = {}
