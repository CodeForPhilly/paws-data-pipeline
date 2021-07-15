def natural_breaks(column, number_of_breaks, labels):
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



    breaks = jenkspy.jenks_breaks(column, nb_class=number_of_breaks)
    labels= labels
    jenks_list = list(pd.cut(column, bins = breaks, include_lowest=True, labels=labels))

    return jenks_list
