def recency_score(dataframe, recency_bins):
    '''
    '''

    import pandas as import pd
    import numpy as np

    recency_score, recency_bins = pd.cut(dataframe['Close_Date'], bins = recency_bins, ret_bins= True)

    return recency_score, recency_bins
