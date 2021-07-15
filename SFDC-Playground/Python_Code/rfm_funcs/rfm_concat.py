def rfm_concat(days_score, frequency_score, amount_score):
    '''
    This function takes in three pandas.series columns and returns a concatenated version of each score for a total rfm score.

    arg1: pandas.series
    arg2: pandas.series
    arg3: pandas.series


    '''
    def concat(a, b, c):
        return int(f"{a}{b}{c}")

    rfm_score = list()
    for ii, jj, kk in zip(days_score, frequency_score, amount_score):
        rfm_score.append(concat(ii,jj,kk))

    return rfm_score
