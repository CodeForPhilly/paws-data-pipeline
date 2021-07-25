def create_scores():
    '''
    '''

    import pandas as pd
    import numpy as np
    from datetime import datetime, date
    from collections import Counter


    df  =pd.read_csv('donations_w_matching_id_20210723.csv')

    df = df.dropna(subset=['amount', 'close_date'])

    # recency

    donations_2021 = df
    donations_2021['close_date'] =pd.to_datetime(donations_2021['close_date']).dt.date
    from data_difference import date_difference

    days = []
    for ii in donations_2021['close_date']:
        days.append(date_difference(ii, '2021-01-01'))
        donations_2021['days_since'] = days

    grouped_2021 = donations_2021.groupby('_id').agg({'days_since': ['min']}).reset_index()

    labels = [5,4,3,2,1]
    grouped_2021['recency_score'] = pd.qcut(grouped_2021[('days_since','min')], q= [0., .2, .4,.6, .8, 1], labels=labels)
