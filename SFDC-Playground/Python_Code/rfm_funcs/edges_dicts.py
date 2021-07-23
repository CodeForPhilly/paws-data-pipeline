def create_bins_dict(recency_edges, recency_labels, frequency_edges, frequency_labels, monetary_edges, monetary_labels):
    '''Create_bins_dict-- creates dictionaries for each edge and label pairing
    This function takes in user defined bin edges and respective labels per each bin edge. User should
    input a list of edges and labels in corresponding order. A set of edges and bins for each score should be entered.

    e.g.
    recency_edges = np.array([0, 1., 2.,4., 10.])
    labels = list(1, 2, 3, 4, 5)
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
