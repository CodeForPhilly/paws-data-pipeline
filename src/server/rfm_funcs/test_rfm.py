# This function is meant to test the RFM create_scores.py function. 

'''
Things needed
1. Create mock data
    a. Mock data must be realistic
    b. mock data must have 5^3 possibilities for RFM score, i.e., 1 RFM score each. 
    c. Therefore we need 125 unique rows.
    d. Recency needs to have at least 5 different dates
    e. Frequency needs to have at least 5 different IDs
    f. Monetary needs to have at least 5 different amounts
    g. Each subject ID will get an RFM score. 
2. create_scores.py will accept this mock data and then generate a new RFM score
3. final step of this function will perform a jaccard similarity analysis to determine if the vectors
match where the result should be exatly 1.0

'''

