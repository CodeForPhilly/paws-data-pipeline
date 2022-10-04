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

Through all of its operational and service activities, PAWS accumulates data regarding donations, 
adoptions, fosters, volunteers, merchandise sales, event attendees (to name a few), 
each in their own system and/or manual tally. This vital data that can 
drive insights remains siloed and is usually difficult to extract, manipulate, and analyze. 

This project provides PAWS with an easy-to-use and easy-to-support tool to extract 
constituent data from multiple source systems, standardize extracted data, match constituents across data sources,  
load relevant data into Salesforce, and run an automation in Salesforce to produce an RFM score. 
Through these processes, the PAWS data pipeline has laid the groundwork for facilitating an up-to-date 360-degree view of PAWS constituents, and 
flexible ongoing data analysis and insights discovery.

## Uses 

- The pipeline can inform the PAWS development team of new constiuents through volunteer or foster engagegement
- Instead of manually matching constituents from volunteering, donations and foster/adoptions, PAWS staff only need to upload the volunteer dataset into the pipeline, and the pipeline handles the matching
- Volunteer and Foster data are automatically loaded into the constituent's SalesForce profile
- An RFM score is calculated for each constituent using the most recent data 
- Data analyses can use the output of the PDP matching logic to join datasets from different sources; PAWS can benefit from such analyses in the following ways: 
    - PAWS operations can be better informed and use data-driven decisions to guide programs and maximize effectiveness;  
    - Supporters can be further engaged by suggesting additional opportunities for involvement based upon pattern analysis;  
    - Multi-dimensional supporters can be consistently (and accurately) acknowledged for all the ways they support PAWS (i.e. a volunteer who donates and also fosters kittens), not to mention opportunities to further tap the potential of these enthusiastic supporters.

## [Code of Conduct](https://codeforphilly.org/pages/code_of_conduct)

This is a Code for Philly project operating under their code of conduct. 

## Links

[Slack Channel](https://codeforphilly.org/chat?channel=paws_data_pipeline)  
[Wiki](https://github.com/CodeForPhilly/paws-data-pipeline/wiki)
