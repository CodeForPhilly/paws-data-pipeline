# rfm_funcs

### Date difference for recency score calculation

# get date difference
def date_difference(my_date, query_date):
    from datetime import datetime, date

    d1 = datetime.strptime(str(my_date), "%Y-%m-%d")
    d2 = datetime.strptime(str(query_date), "%Y-%m-%d")
    diff = (d2 - d1)
    return diff





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



def merge_series(list1, list2):

    merged_list = tuple(zip(list(list1), list(list2)))
    return merged_list
