def recency_bins(donations_df, query_date):
    ''' takes the grouped dataframe and outputs bin edges for recency scores
    for the entire data history.
    '''

    from date_difference import date_difference
    days = []
    for ii in donations_df['Close_Date']:
        days.append(date_difference(ii, str(query_date)))

    donations_2021['days_since'] = days


    donations_df = donations_2021.groupby('Contact ID 18').agg({'days_since': ['min']}).reset_index()

    labels = [5,4,3,2,1]

    donations_df['recency_score'], bins = pd.qcut(donations_df[('days_since','min')], q= [0., .2, .4,.6, .8, 1], labels=labels, ret_bins = True)


    quantile_score = donations_df[('days_since','min')].quantile([.2, .4,.6, .8, 1])


    return recency_bins, quantile_scores
