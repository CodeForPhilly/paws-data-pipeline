def frequency_score(donations_df, number_of_breaks):
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



    donations_df_grouped = donations_df.groupby([df['Contact ID 18'], df['Close_Date'].map(lambda x: x.year)]).count().max(level=0) #### NEED TO CHANGE THIS TO LAST 90 DAYS OR THE LAST QUARTER

    
    donations_df_grouped = donations_df_grouped.reset_index()

    df_frequency = donations_df_grouped[['Contact ID 18' ,'Close_Date']]

    import jenkspy

    breaks = jenkspy.jenks_breaks(df_frequency['Close_Date'], nb_class=5)
    labels= range(1,6)
    df_frequency['frequency_score'], bins = pd.cut(df_frequency, bins = breaks, include_lowest=True, labels=range(1,6), ret_bins = True)

    return df_frequency, frequency_bins
