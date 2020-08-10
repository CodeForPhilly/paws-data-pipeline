# [The Philadelphia Animal Welfare Society (PAWS)](phillypaws.org)

As the city's largest animal rescue partner and no-kill animal shelter, 
the [Philadelphia Animal Welfare Society (PAWS)](phillypaws.org) is working to make Philadelphia 
a place where every healthy and treatable pet is guaranteed a home. Since inception over 10 years ago, 
PAWS has rescued and placed 27,000+ animals in adoptive and foster homes, and has worked to prevent pet homelessness 
by providing 86,000+ low-cost spay/neuter services and affordable vet care to 227,000+ 
clinic patients. PAWS is funded 100% through donations, with 91 cents of every dollar collected going 
directly to the animals. Therefore, PAWS' rescue work (including 3 shelters and all rescue and 
animal care programs), administration and development efforts are coordinated by only about 
70 staff members complemented by over 1500 volunteers.

## [The Data Pipeline](https://codeforphilly.org/projects/paws_data_pipeline)

This project seeks to provide PAWS with an easy-to-use and easy-to-support tool to extract 
data from multiple source systems, confirm accuracy and appropriateness, 
clean/validate data where necessary (a data hygiene and wrangling step), 
and then load relevant data into one or more repositories to facilitate 
(1) a highly-accurate and rich 360-degree view of PAWS constituents 
(Salesforce is a likely candidate target system; already in use at PAWS) and 
(2) flexible ongoing data analysis and insights discovery (e.g. a data lake / data warehouse). 

Through all of its operational and service activities, PAWS accumulates data regarding donations, 
adoptions, fosters, volunteers, merchandise sales, event attendees (to name a few), 
each in their own system and/or manual (Google Sheet) tally. This vital data that can 
drive insights remains siloed and is usually difficult to extract, manipulate, and analyze. 
Taking all of this data, making it readily available, and drawing inferences through analysis 
can drive many benefits:   

- PAWS operations can be better informed and use data-driven decisions to guide programs 
and maximize effectiveness;  
- Supporters can be further engaged by suggesting additional opportunities for involvement 
based upon pattern analysis;  
- Multi-dimensional supporters can be consistently (and accurately) acknowledged for all 
the ways they support PAWS (i.e. a volunteer who donates and also fosters kittens), 
not to mention opportunities to further tap the potential of these enthusiastic supporters.

## [Code of Conduct](https://codeforphilly.org/pages/code_of_conduct)

This is a Code for Philly project operating under their code of conduct. 

## Getting started
see [Getting Started](GettingStarted.md) to run the app locally

## Project Plan

### Phase 1 (now - Jan 15 2020) 

**Goal**: Create a central storage of data where 

1. Datasets from top 3 relevant sources can be uploaded as csvs to a central system: a) Donors, b) Volunteers, 
c) Adopters
2. All datasets in the central system can be linked to each other on an ongoing basis
3. Notifications can be sent out to relevant parties when inconsistencies need to be handled by a human
4. Comprehensive report on a person’s interactions with PAWS can be pulled via a simple UI (must include full known history)

### Phase 2 (Jan 15 - May 15 2020)

**Goal**: Expand above features to include all relevant datasets and further automate data uploads
Datasets from all other relevant sources can be uploaded as csvs to a central system ( a) Adoption and Foster applicants, 
b) Foster Parents, c) Attendees, d) Clinic Clients e) Champions, f) Friends)
Where APIs exist, create automated calls to those APIs to pull data

### Phase 3 (May 15 - Sept 15 2020)

**Goal**: Create more customizable analytics reports and features (eg noshow rates in clinicHQ)

## Links

[Slack Channel](https://codeforphilly.org/chat?channel=paws_data_pipeline)

[Google Drive](https://drive.google.com/open?id=1O8oPWLT5oDL8q_Tm4a0Gt8XCYYxEIcjiPJYHm33lXII) 