def create_bins_dict(recency_edges, recency_labels, frequency_edges, frequency_labels, monetary_edges, monetary_labels):
    '''

    '''

    recency_dict = {}
    for ii,jj in zip(recency_labels, recency_edges):
        recency_dict["{0}".format(ii)] = jj

    frequency_dict = {}
    for tt,kk in zip(frequency_labels, frequency_edges):
        frequency_dict["{0}".format(tt)] = kk


    monetary_dict = {}
    for ww,hh in zip(monetary_labels, monetary_edges):
        monetary_dict["{0}".format(ww)] = hh


    return recency_dict, frequency_dict, monetary_dict
