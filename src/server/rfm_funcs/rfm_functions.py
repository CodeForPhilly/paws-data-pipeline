# rfm_funcs

### A number of RFM functions which are called by the main create_scores function.

def date_difference(my_date, query_date):
    '''
    This function takes in a single date from the donations dataframe (per row) and compares the difference between that date and the date in which matching occurs.
    I.e. pipeline matching should provide a query_date so that this can work.
    '''
    from datetime import datetime, date

    d1 = datetime.strptime(str(my_date), "%Y-%m-%d")
    d2 = datetime.strptime(str(query_date), "%Y-%m-%d")
    diff = (d2 - d1)
    return diff





def rfm_concat(days_score, frequency_score, amount_score):
    '''
    This function takes in three pandas.series columns and returns a concatenated version of each score for a total rfm score.
    Assumes that arg1 are Recency, arg2 are Frequency and arg3 are Monetary values
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
    '''
    This function takes in two tuples and merges them into a list of tuples.
    '''
    merged_list = tuple(zip(list(list1), list(list2)))
    return merged_list



def create_bins_dict(recency_edges, frequency_edges, monetary_edges):
    '''
    Create_bins_dict-- creates dictionaries for each edge and label pairing
    This function takes in user defined bin edges and respective labels per each bin edge. User should
    input a list of edges and labels in corresponding order. A set of edges and bins for each score should be entered.

    e.g.
    recency_edges = np.array([0, 1., 2.,4., 10.])
    '''

    recency_dict = {}
    recency_labels = list(5,4,3,2,1)
    for ii,jj in zip(recency_labels, recency_edges):
        recency_dict["{0}".format(ii)] = jj

    frequency_dict = {}
    frequency_labels= list(1,2,3,4,5)
    for tt,kk in zip(frequency_labels, frequency_edges):
        frequency_dict["{0}".format(tt)] = kk


    monetary_dict = {}
    monetary_labels = list(1,2,3,4,5)
    for ww,hh in zip(monetary_labels, monetary_edges):
        monetary_dict["{0}".format(ww)] = hh


    return recency_dict, frequency_dict, monetary_dict
