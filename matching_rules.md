The logic for looking at duplicates from Karla/Meg discussion:

1. Create Master from Salesforce
2. Compare Volgistics to Master: If [fuzzy match on name above threshold] and [match on email] → combine records in Master
3. Compare Master to PetPoint: If [fuzzy match on name above threshold] and [match on email] → combine records in Master
4. Compare Master to ClinicHQ: If [fuzzy match on name above threshold] and [match on phone number] → combine records in Master

Trigger staff review: If [fuzzy match on name above threshold] and [no other matching data] → report for human review

Thresholds are TBD but should be some level where we can be reasonably certain the fuzzy match is correct most of the time.
Decided to trust name and email most. Addresses will likely create more problems with fuzzy matching, allowing people in the same household (but not the same person) to potentially be matched. Email is likely to be unique per person, though the same person *may* use multiple emails. 
