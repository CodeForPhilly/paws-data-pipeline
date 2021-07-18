def create_bins(csv, query_date):
    '''This script will take csv files and bin edges for RFM scores for all PAWS donations
    csv = path to csv file as string
    query_date = date data was queried
    '''

    import pandas as pd
    import numpy as np
    import jenkspy
    from datetime import datetime, date
    import os



    ####
    # read in csv
    donations_df = pd.read_csv('csv')

    donations_df['Close_Date'] =pd.to_datetime(donations_2021['Close_Date']).dt.date

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
    # Write bins to a txt files
    today = date.today()

    file1 = open("rfm_bins" + str(today) + ".txt","a")
    file1.writelines('Recency:')
    file1.writelines('Recency bins:' + recency_bins)
    file1.writelines('Recency bins: quantile scores:' +quantile_scores)
    file1.writelines('Frequency:')
    file1.writelines('Jenks Frequency Bins:' + jenks_frequency_bins)
    file1.writelines('Human Frequency Bins:' + human_frequency_bins)
    file1.writelines('Amount:')
    file1.writelines('Amount Jenks Bins:' + amount_jenks_bins)
    file1.writelines('Human Amount Bins:'+ human_amount_bins)
    file1.close()
