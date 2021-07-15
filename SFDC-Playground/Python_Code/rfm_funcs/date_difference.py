# get date difference
def date_difference(my_date, query_date):
    from datetime import datetime, date

    d1 = datetime.strptime(str(my_date), "%Y-%m-%d")
    d2 = datetime.strptime(str(query_date), "%Y-%m-%d")
    diff = (d2 - d1)
    return diff
    
