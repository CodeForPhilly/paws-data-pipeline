# RFM

## RFM Data Flows

![](<../.gitbook/assets/image (3).png>)

## RFM Database Tables

![](<../.gitbook/assets/image (4).png>)

## RFME Bin Logic

### Recency:

If a person's last donation was:

* the last 180 days: R = 5,
* 180-365 days ago: R = 4
* 365 - 728 days ago: R = 3,
* 728 - 1093 days ago: R = 2
* More than 0: R = 1
* Never given: R = 0

### Frequency:

If in the last 24 months someone has made a total of

* 24 or more donations: F = 5,
* 12 - 23 donations: F = 4
* 3 - 11 donations: F = 3
* 2 donations: F = 2;
* 1 donation: F = 1
* 0 donations: F = 0

### Monetary value:

If someone's cumulative giving in the past 24 months is

* $2001 ore more: M = 5
* $501 - $2000: M = 4
* $250 - $500: M = 3
* $101 - $249: M = 2
* $25 - $100 - $50: M = 1
* $0 - 25: M = 0

### the impact labels are as follows:

* High impact: (F+M)/2 is between 4-5
* Low impact: (F+M)/2 is between 1-3

### the engagement labels are as follows:

* engaged: R = 5
* slipping: R is 3-4
* disengaged: R is 1-2

### CAN WE INTEGRATE SCORING FOR FOSTERS/VOLUNTEERS?

"RFME" (E FOR ENGAGEMENT)

* volunteered or fostered in the past 30 days: E = 5
* volunteered or fostered in the past 6 months days: E = 4
* volunteered or fostered in the past year: E = 3
* volunteered or fostered in the past 2 years: E = 2
* volunteered or fostered ever: E = 1
* volunteered or fostered never: E = 0

(modified from Lauren's request of: E = 5 (CURRENT), E = 4 (WITHIN THE PAST YEAR), E = 3 (WITHIN THE PAST TWO YEARS), E = 2 (EVER), E = 0 (NEVER), because "1" value was missing and needed more specific definition of "current")
