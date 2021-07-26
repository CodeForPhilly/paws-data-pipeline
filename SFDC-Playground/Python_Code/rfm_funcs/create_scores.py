def create_scores():
    '''
    '''

    import pandas as pd
    import numpy as np
    from datetime import datetime, date
    from collections import Counter


    df  =pd.read_csv('donations_w_matching_id_20210723.csv')

    df = df.dropna(subset=['amount', 'close_date'])

    # read in labels and bin edges from table

    recency_labels = [5,4,3,2,1]
    recency_bins =                  #        imported from table

    frequency_labels= [1,2,3,4,5]
    frequency_bins =                #       imported from table

    monetary_labels= [ 1,2,3,4,5]
    monetary_bins =                 #       imported from table


    # recency


    donations_2021 = df
    donations_2021['close_date'] =pd.to_datetime(donations_2021['close_date']).dt.date

        # calculate date difference between input date and
    from rfm_functions import date_difference
    days = []
    for ii in donations_2021['close_date']:
        days.append(date_difference(ii, '2021-01-01'))
        donations_2021['days_since'] = days

    grouped_2021 = donations_2021.groupby('_id').agg({'days_since': ['min']}).reset_index()


    grouped_2021['recency_score'] = pd.cut(grouped_2021[('days_since','min')], bins= recency_bins, labels=recency_labels, include_lowest = True)



    # frequency

    df['close_date'] = pd.DatetimeIndex(df['close_date'])

    df_grouped = df.groupby(['matching_id', pd.Grouper(key = 'close_date', freq = 'Q')]).count().max(level=0)

    df_grouped = df_grouped.reset_index()


    df_frequency = df_grouped[['matching_id' , 'opp_id']]

    df_frequency['frequency_score'] = pd.cut(df_frequency['opp_id'],
                                               bins = frequency_bins, labels=frequency_labels, include_lowest=True)



    # amount

    df_amount = df.groupby(df['matching_id'], as_index=False).amount.max()

    df_amount['amount_score'], bins = pd.cut(df_amount['amount'], bins= monetary_bins, include_lowest=True, labels = monetary_labels)


    # Concatenate rfm scores
        # merge monetary df and frequency df
    df_semi = df_amount.merge(df_frequency, left_on='matching_id', right_on= 'matching_id')
        # merge monetary/frequency dfs to recency df
    df_final = df_semi.merge(grouped_2021, left_on='matching_id', right_on= 'matching_id')

    # import function: rfm_concat, which will catenate integers as a string and then convert back to a single integer
    from rfm_functions import rfm_concat
    df_final = rfm_concat(df_final[('recency_score'),''], df_final['frequency_score'], df_final['amount_score'])

    # Append rfm score to final df
    df_final['rfm_score'] = rfm_score

    from rfm_functions import merge_series
    score_tuples = merge_series((df_final['matching_id']), df_final['rfm_score'])

    return score_tuples
