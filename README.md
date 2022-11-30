# Project Overview

## [The Philadelphia Animal Welfare Society (PAWS)](https://github.com/CodeForPhilly/paws-data-pipeline/blob/master/phillypaws.org)

As the city's largest animal rescue partner and no-kill animal shelter, the [Philadelphia Animal Welfare Society (PAWS)](https://github.com/CodeForPhilly/paws-data-pipeline/blob/master/phillypaws.org) is working to make Philadelphia a place where every healthy and treatable pet is guaranteed a home. Since inception over 10 years ago, PAWS has rescued and placed 27,000+ animals in adoptive and foster homes, and has worked to prevent pet homelessness by providing 86,000+ low-cost spay/neuter services and affordable vet care to 227,000+ clinic patients. PAWS is funded 100% through donations, with 91 cents of every dollar collected going directly to the animals. Therefore, PAWS' rescue work (including 3 shelters and all rescue and animal care programs), administration and development efforts are coordinated by only about 70 staff members complemented by over 1500 volunteers.

This project seeks to provide PAWS with an easy-to-use and easy-to-support tool to extract data from multiple source systems, confirm accuracy and appropriateness, clean/validate data where necessary (a data hygiene and wrangling step), and then load relevant data into one or more repositories to facilitate (1) a highly-accurate and rich 360-degree view of PAWS constituents (Salesforce is a likely candidate target system; already in use at PAWS) and (2) flexible ongoing data analysis and insights discovery (e.g. a data lake / data warehouse).

Through all of its operational and service activities, PAWS accumulates data regarding donations, adoptions, fosters, volunteers, merchandise sales, event attendees (to name a few), each in their own system and/or manual (Google Sheet) tally. This vital data that can drive insights remains siloed and is usually difficult to extract, manipulate, and analyze. Taking all of this data, making it readily available, and drawing inferences through analysis can drive many benefits:

PAWS operations can be better informed and use data-driven decisions to guide programs and maximize effectiveness; Supporters can be further engaged by suggesting additional opportunities for involvement based upon pattern analysis; Multi-dimensional supporters can be consistently (and accurately) acknowledged for all the ways they support PAWS (i.e. a volunteer who donates and also fosters kittens), not to mention opportunities to further tap the potential of these enthusiastic supporters.

### [The Data Pipeline](https://codeforphilly.org/projects/paws\_data\_pipeline)

Through all of its operational and service activities, PAWS accumulates data regarding donations, adoptions, fosters, volunteers, merchandise sales, event attendees (to name a few), each in their own system and/or manual tally. This vital data that can drive insights remains siloed and is usually difficult to extract, manipulate, and analyze.

This project provides PAWS with an easy-to-use and easy-to-support tool to extract constituent data from multiple source systems, standardize extracted data, match constituents across data sources,\
load relevant data into Salesforce, and run an automation in Salesforce to produce an RFM score. Through these processes, the PAWS data pipeline has laid the groundwork for facilitating an up-to-date 360-degree view of PAWS constituents, and flexible ongoing data analysis and insights discovery.

### Uses

* The pipeline can inform the PAWS development team of new constiuents through volunteer or foster engagegement
* Instead of manually matching constituents from volunteering, donations and foster/adoptions, PAWS staff only need to upload the volunteer dataset into the pipeline, and the pipeline handles the matching
* Volunteer and Foster data are automatically loaded into the constituent's SalesForce profile
* An RFM score is calculated for each constituent using the most recent data
* Data analyses can use the output of the PDP matching logic to join datasets from different sources; PAWS can benefit from such analyses in the following ways:
  * PAWS operations can be better informed and use data-driven decisions to guide programs and maximize effectiveness;
  * Supporters can be further engaged by suggesting additional opportunities for involvement based upon pattern analysis;
  * Multi-dimensional supporters can be consistently (and accurately) acknowledged for all the ways they support PAWS (i.e. a volunteer who donates and also fosters kittens), not to mention opportunities to further tap the potential of these enthusiastic supporters.

### [Code of Conduct](https://codeforphilly.org/pages/code\_of\_conduct)

###

##
