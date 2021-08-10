def amount_bins(donations_df, amount_binvals):
    '''
    '''

    import jenkspy

    big_donations = donations_df[donations_df['Amount'] >= 50]

    amount_jenks_bins = jenkspy.jenks_breaks(big_donations['Amount'], nb_class=5)
    labels = range(1,6)
    amount_jenks_bins



    # human_amount_bins = big_donations[['Amount']].quantile([.2,.4,.6,.8]).reset_index()


    # human_amount_bins = bins[['Amount']].to_numpy().flatten()
    # lower_bin = 0
    # upper_bin = np.inf
    # human_amount_bins = np.insert(bins, 0, lower_bin)
    # human_amount_bins = np.insert(bins, 5, upper_bin)

    return amount_jenks_bins, amount_binvals
