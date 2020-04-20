# PAWS Data Pipeline Narrative (updated 4/20/20)

## Overall Description

PAWS uses multiple software (cloud-based) systems to support its various operating needs.  Information on PAWS constituents is spread across these **Operational Systems** with varying levels of consistency (/inconsistency) in how they are represented.

This is supposed to be a diagram, but I am not sure how to get it to work
![alt text](https://github.com/CodeForPhilly/paws-data-pipeline.git/documentation/PAWS_Digital_Ecosystem_v3_for_C4P.jpg "Diagram")

Two objectives are:

1.  A 360-degree view of constituents is important for PAWS to be able
to (1) fully understand the depth and breadth of constituent engagement;(2) accurately acknowledge the various aspects of support provided by individuals; and (3) encourage, invite and inspire further engagement across PAWS' various programs and opportunities to extend involvement in and support for PAWS mission.

2.  PAWS is increasingly interested in using data to better understand,
measure, and tune their operating processes.  Each study requires harversting and wrangling data from one or more sources before any analyis can be done.  Having data from each system regularly extracted and prepped (cleaned, matched, etc) for analysis would speed such projects as they arise and directly support repeated analyses over time.  

## Systems View - Summary

PAWS uses multiple **Operational Systems** to support its various operating needs.

    Salesforce - Fund raising
    Volgistics - Volunteer management 
    Petpoint - Animal management
    ClinicHQ - medical records for clinic patients (animals)
    iContact - email marketing
    Trello - workflow management
    (there are more... just not pertinent to our initial work)
    
Information on PAWS constituents is spread across these various systems. Often the same constituent shows up in multiple systems with no guarantee as to how consistently they are represented (i.e. name, address, email, etc could be different, misspelled, or of different vintage - pre/post marriage, house move, etc).   Sometimes a constituent shows up on only one system.   All constituents are important.

Each of these **Operational Systems** is ideally suited to what it does. There is not a single system that can meet all various operating needs. Thus we are in a **multi-system** situation. 

## Envisioned Repositories
1. Salesforce's built-for purpose is as a constituent management system.  PAWS should use it in this way. Namely, all aspects of a constituent's relationship with PAWS should be **visible** in Salesforce tothe extent that such information helps to comprehend the 360-degree relationship (while **not** strictly duplicating **all** information in the various other Operational Systems).

2. It seems like a "Data Lake" would be valuable to hold detail information from all Operational Systems in a way that makes it readily available for ongoing analysis.   This would be used by data scientists to develop analyses and perhaps by PAWS staff running pre-developed scripts to update existing analyses.  This would not be an end-user reference system.   End-user access is via the Operational Systems, with Salesforce focused on constituent information. 
  
## Use Cases
### Use Case:  Data Loading
- PAWS Staff (or authorized volunteer) would export current-period transaction data from given **Operational Systems**.  (see note 1)
- PAWS Staff would upload exported data for further processing into the PAWS Data Pipeline.  (see note 1)
- A routine would be triggered to in-process the new datasets, flagging any exceptions and providing a way for interaction to clear conflicts / exceptions (see note 2)
- A routine would be triggered to load data to target systems.  This step is dependent upon clearing of conflicts from prior step.

Note 1:  for systems without API trigger capability, this could be automated through UI automation tools.    That's a TBD for later.  For systems with API capabilites, this could be scheduled without user involvement provided timeframe selection can be programmed.  When automated, uploading is similarly automatable.

Note 2:  presence of new files could be detected and routines automatically run.  Also, routines could be cron run at given times.

### Use Case: PAWS Staff Member Examines a Constituent
- PAWS could pull up a constituent in Salesforce and see thier contact information, their donation activity, their volunteer activity, their adoption and fostering activity, and their clinic visit activity - all at an appropriate level of detail.  
- From this single review of their **Contact** record in Salesforce, the user can assess the relationship.   
- They can go deeper in Salesforce for Donation Info and can look at other Operational systems for extended detail.  
- Where possible, hyperlinking to other Operational systems should be included in Salesforce to ease finding more details information.

### Use Case:  PAWS Identifies Constituents for Campaigns or Outreach
- PAWS staff person uses criteria to extract (or flag) constituents in Salesforce meeting certain criteria (e.g. volunteers that have not donated, new adopters in last 12 months, clinic visits in last six months, etc) with the intent to engage them further (solicit donation, inquire about interest in volunteering, etc).
- PAWS staff person takes this information and loads up an email marketing or mail-merges a U.S. Mail mailing.  

### Use Case: Data Scientist
- The data scientist and PAWS engage on the analysis needed
- The data scientist inspects the Data Lake for relevant data for the study at hand based upon source Operational
systems and analysis required
- If the data is not present, a project is initiated to identify, gather, and include such data in
the Data Lake
- If data is present, the Data Scientist uses Python, R, or other tools of choice to extract data and perform analysis

## MVP's / Proof Points

Along the way to functional releases of production solution components, development will be through a series of MVP's leading to Proof Points of functionality.  In this way we can iteratively build toward the solution without requiring all surrounding pieces (including to-be-developed pieces!) to be in place during the development cycle.

### MVP 1:  Loading Files In/Out of Code-for-Philly (C4P) Infrastructure [NEARLY DONE]
- Web interface to select and load files, view file list on server, pull down files as needed
- Underlying database to hold files that survives container restart

### MVP 2:  Identifying & Enriching Contacts in Imported Files [IN EARLY STAGES]
- Prerequisites:  MVP1, Schema for Master Table
- Run matching routine
- For known contacts, enrich uploaded dataset with PAWS Data Pipeline (PDP) identifiers
- For new contacts, populate the master table and enrich records with PDP identifiers.  
- For ambiguous contacts (uncertain if known or unknown), gather possible matches or, in general, what the matching routine tell us (**team closest to matching routine to advise**)
- Provide web interface to review and resolve ambiguous records.  Resolution actions include:  (1) we know this person, and their PDP ID is xxxxx; (2) we don't know this person so create it as new in PDP master table. 
- As contacts are matched (and resolved), create staging table in database of enriched records ready for further processing
- Log all above activity for tracking.  Consider creating master log with various record types for each type of event 
- Provide easy-to-read report (or web interface) to review log of activity

### MVP 3:  Data Lake Imports from Staging Tables
- Prerequisites:  MVP 1, MVP 2
- Create schema for Data Lake tables - one per data source (perhaps more)
- From staging tables, identify the data source and information being loaded
- Load into data lake area for that data source (i.e. Volgistics, Petpoint, ...) 
- Provide web interface to examine data in the Data Lake - simple canned queries

### MVP 4:  Run Iterative Data Loads (Simulate Real Use)
- Prerequisites:  MVP's 1 - 3
- Get data from PAWS systems from multiple time periods
- For each given time period, run solutions from MVP 1, MVP 2, and MVP 3 as they are envisioned to be run in production use.  Evaluate user experience, process integrity, results.  
- Cycle back on any issues and work to resolution.    

### MVP 5:  Simulate Connected Data
- Prerequisites: MVP's 1-4
- Develop queries to combine data from sources into a constituent view (all records associated with a given contact)
- Provide simple rudimentary web interface to show 360-degree view based upon data collected so far.  

### MVP 6:  Salesforce Prototyping
- Prerequisites: MVP's 1-5
- To be defined.   When we've done 1-5 we will know how our data relates and that we have a good constituent view.  

## Operational System Details

Each of the Operational Systems in use at PAWS is a source for data regarding constituents.   Each is explored below

### Salesforce
Salesforce receives donation information from **Classy**, PAWS' online donation platform.  An API connects Classy & Salesforce.  When new donations flow into Salesforce, it tries to match to existing Contacts using match logic in Classy and Salesforce.  If a match is found it associates the new donation with the existing Contact.   If a match is not found, it triggers creation of a new Contact and a corresponding Household (Organization object, repurposed and renamed to Household in the Salesforce Non-Profit Success Pack).

Donations can also be manually entered into Salesforce.  In this case, staff enters donation information accordingly, creating Contact and Household records if necessary to create the donor to associate the donation with.

The Development (i.e. Fund Raising) team w/in PAWS also utilizes **Call** and other objects w/in Salesforce to track their interactions with constituents (i.e. Contacts in Salesforce).  

Salesforce also receives (via API) notification from **iContact** when marketing / solicitation emails are sent and when contacts open them.    This is similarly matched/added by contact.   

All of the above information is stored as objects in Salesforce and are viewable via the Contact and Household objects.    E-Mail campaign information is also viewable via Campaigns w/in Salesforce.  

Presence of Donation information associated with a given contact indicates that the constituent is a donor to PAWS. 

Salesforce is mostly a target system for this project, wherein we are seeking to associate information from other Operational Systems to the consituents already in Salesforce and to add contacts and associated information from source systems where they do not already exist in Salesforce.     

Salesforce is a source system for known consituents (Contacts) into the *Matching Process*, to be discussed later in this document. 

Salesforce provides for file export and import as well as rich API-driven data import/export and process triggers.    
   
### Volgistics
All activities requiring volunteer staffing are set up in Volgistics by PAWS Volunteer Coordinator (a staff position).  

Volunteers are set up in Volgistics once they complete a volunteer orientation session.  Their ID is the email address they supply.   They are sent a link and must set up a password as part of their initial sign-in.  

Via the Volgistics website Volunteers can view open shifts in skill areas they have been oriented on and sign up as they wish.  Work shifts exist across all three PAWS locations, remote work (administrative activities), and hundreds of events held across Philadelphia and surrounding area.  

Volunteers log shifts and hours worked by either signing in on a tablet (running a Volgistics "app") at one of the three PAWS sites or by manually entering shifts worked via the Volgistics website.   

Volgistics does not have API capabilities.   

Volgistics does offer csv-based export triggered via it's web-based adminsitrative user interface.  For shifts worked, the file export is two files:  One file lists the volunteer identifying information (name, email address, etc, along with an ID number); the other file lists each shift worked with each shift record referencing the volunteer's ID number.  

Volgistics is a source system for this project.  By exporting volunteer shifts worked data it is possible to add these to Salesforce, matching to existing Contacts or adding Contacts (and associated Household) as required.  By doing this, a summary (and some detail) of Volunteer Shifts and Hours Worked is visible on constituent Contact recrods.   At a high level, presence of Volunteer Hours worked indicates that the constituent has been (and/or is currently) a PAWS Volunteer.  

It's envisoned that a PAWS staff member or a designated Volunteer would export new shifts-worked data from Volgistics for loading into the PAWS Data Pipeline, with these records ending up in the Data Lake in a format for analysis over time and into Salesforce as Volunteer Shifts worked associated with appropriately-matched Contacts via the *Matching Process*.    The file export may be scriptable via UI automation (simulating screen interactions) as a future innovation.   In any case, a location to upload the CSV files to is required, as is a way to trigger an import process.  

### Petpoint
Petpoint is used to track animals.   It is used by Philadelphia ACCT, the open-intake animal shelter and thus is also used by animal rescue organizations in the area since, through use of this common system, all demographic and health record information follows the animal through it's rescue-foster-adoption cycle.   An animal transfer between participating organizations is reflected via simple reassignment in Petpoint without the need for cross-system data transcription.  

Petpoint is used by animal welfare staff in all organizations that an animal passes through.   At PAWS, it is used by kennel, medical, foster, and adoption staffs for inquiry and logging of new information during the animal's time with PAWS. 

Animals in Petpoint have a unique "A" number (animal numbers start with an "A" followed by a string of numbers).  

Petpoint data must be better understood as part of this project.  Current thinking is below.

**The intent** is to use Petpoint data to show fostering and adopting history as part of a constituent's Contact record in Salesforce.   

Contact processing is fairly straightforward.  Extracting foster-parenting and adopting contact information from Petpoint, taking it through the *Matching Process*, and loading it into Salesforce would ensure that we have awareness of every fostering or adoptive person.   

Animals processing and associating them appropriately with contacts is more complex.  Animals can move between people.  A given animal can be fostered sequentially by multiple different people, an animal can be adopted, an adopted animal can be returned, and then that same animal can be fostered and/or adopted again.   Thus, merely listing the animal on a contact record won't show accurate information.   It is not a 1:1 person:animal relationship.

Updated Solution April 2020:
 - Animal adoption and fostering instances would be identified from Petpoint.  
 - Each adoption/fostering instance would be associated with the corresponding human contact from PAWS Data Pipeline master table (and thus linking to contact instances in Salesforce and other repositories)
 - A set of fields will be set up on the Salesforce Contact object for instances of adoptions/fosters
 - Adoption/Foster instances will be added to the appropriate contacts in Salesforce, listing the date of placement.

Notes on this approach:
 - a given animal can be associated with different people across time.  This is fine.
 - this solution shows animal placement events.  It does not show animal lifecycle nor does it assert currency of relationship between animal and contact.  It only asserts that an adoption/fostering placement occurred between animal and contact. 
 - this information is useful to show adoption/fostering HISTORY for contacts.   This is useful to profile the contact's relationship with PAWS.   

Elegant Solution (Future):
 - an "Animal" custom object would be configured within Salesforce.   
 - An extract from Petpoint would be processed to identify animals as a list of "A" numbers and cursory demographics on each animal (such as A12345 is Brutus and he's a Pit Mix dog). 
 - Animal data would be loaded into Salesforce.   
 - The extract from Petpoint would also be processed to identify who currently has the animal.   
 - That contact would be run through the *Matching Process* and when the corresponding Salesforce contact is identified (or a new one added if no match) a link record would be created to connect the animal and contact at this point in time with datetime stamping start-of-connection and eventual end of connection (for fosters or adoption returns).  
 - By viewing a contact in Salesforce you would see each animal that this contact has had a relationship with - both fostering and adopting.  This is valuable information to further understand how a constituent interacts with PAWS. 
 
 ### ClinicHQ
 ClinicHQ is used by PAWS low-cost clinic to track visits to the clinic and vet doctor notes. 
 
 Very little work has been done with ClinicHQ data.   
 
 It is envisioned that occurrences of clinic visits (not details, but logging that someone visited the clinic) could be pulled from ClinicHQ exports and loaded into Salesforce to further elaborate the relational contacts with that constituent.   
 
 More work must be done here.
 
 ### Trello
 Trello is used to manage many workflows at PAWS.   It's very easy to use and has been embraced by the adoption and fostering application vetting and animal/person matching process.  
 
 Unfortunately data in this system lacks precision when it comes to names, spellings, email addresses, etc.    Also, extracting the data and processing through the JSON output is complex.  
 
 This data has been used to analyze time-to-place animals including time-to-complete each step and overall touches.   It would be useful to format this data for easier ongoing analysis in the Data Lake.   There **does not** appear to be data here that would have utility as part of the Salesforce contact record.  

## The Matching Process

The Code for Philly PAWS team has spent considerable time on how best to match contacts across the various systems.    

Constituents each may be known differently in the various **Operational Systems** at PAWS.  Instead of insisting that PAWS refer to people consistently across all systems, we feel the more practical approach is to create a *Matching Table* that will contain the known identities of each constituent in every PAWS systems they appear in (Salesforce, Volgistics, Petpoint, ClinicHQ).  It would also contain a unique PAWS Data Pipeline identifier (number) for each constituent.

A matching routine can be run on contacts appearing on transactional records (donations, volunteer shifts, fostering, adopting, ...) from PAWS' **Operational Systems** as those records come into the PAWS Data Pipeline, identify whether the contact is clearly known already, clearly new, or that further inspection is needed to determine known or new.   

Contacts without matching certainty will require human review.   The best people to help resolve these is PAWS staff.  **Therefore, some report or online screen-based display of these must be made available.**  It will be important to show the underlying data and any possible matches that our process is contemplating.  For instance, if the contact's source is a donation the donation detail should be readily reviewable.   Likewise if it's a volunteer shift then the shift detail would help understand who it really is.  
 
The *Matching Table* would be maintained and curated over time.  Contacts may change (marry, divorce, move, change emails, etc) over time.   Continuity is required in these cases.  

## Downstream Processing

As discussed prior, transactional data coming into the PAWS Data Pipeline will be used for two purposes:  (a) creating a 360-degree constituent view in Salesforce and (b) populating a Data Lake for ongoing analytical work.   

Disambiguating the contact associated with each record being processed is common to both, and should be performed first (including any manual resolution that is needed).    In this way, the Salesforce contact form can be added to the records that are destined for Saleforce upload and the PAWS Data Pipeline identifier can be added for inclusion in the Data Lake.   Quite possibly more information from the Matching Table may be useful for Data Lake inclusion.  

### Salesforce 360-Degree View
A processing routine will be needed for each type of transactional record (donation, volunteer shift, adoption/foster, etc).   Data would originate through the outloads from source systems, go through the **Matching Process** and then be loaded appropriately into and linked within Salesforce.  

### Data Lake
A processing routine will be needed for each type of transactional record heading into the Data Lake.   This is where more complex records (Trello, if we get to it!) will be decoded and stored in a way that facilitates analysis (i.e. run through the JSON once, now, to ease analysis later).  






