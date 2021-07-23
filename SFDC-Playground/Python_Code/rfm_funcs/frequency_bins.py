def frequency_bins(donations_df, number_of_breaks, frequency_binvals):
    '''
    This function uses the jenkspy package to create natural break points in a dataframe column. Jenkspy attempts to maximize bretween break variance while minimizing within break variance and is similar to Fisher's Discrimenant analysis.
    It returns a list of breakpoints in the order of the original column which can then be appended to any dataframe

    The use of this script requires a pandas dataframe column as arg1:column and the number of breaks to create as arg2:number_of_breaks. Arg3 is a list of strings or range type object

    [license and other info](https://anaconda.org/conda-forge/jenkspy)
    info on (jenks natural breakpoints)[https://en.wikipedia.org/wiki/Jenks_natural_breaks_optimization]


    column:pandas.series---e.g., df['column_name']
    number_of_breaks:int ---e.g., 5
    lables: list of strings or range type object---e.g., list(small, medium, large), range(1,6)



    '''
    import jenkspy


    donations_df['Close_Date'] = pd.DatetimeIndex(df['Close_Date'])
    df_grouped = donations_df.groupby(['Contact ID 18', pd.Grouper(key = 'Close_Date', freq = 'Q')]).count().max(level=0)
    df_grouped = df_grouped.reset_index()
    df_frequency = df_grouped[['Contact ID 18' ,'Close_Date']]


    jenks_frequency_bins = jenkspy.jenks_breaks(df_frequency['Close_Date'], nb_class=5)



    human_frequency_bins= frequency_binvals




    return jenks_frequency_bins, human_frequency_bins
