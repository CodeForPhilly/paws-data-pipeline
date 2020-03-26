
## Overall Description

PAWS uses multiple software (cloud-based) systems to support its various operating needs.  Information on PAWS constituents is spread across these **Operational Systems** with varying levels of consistency (/inconsistency) in how they are represented.

!PAWS_Digital_Ecosystem_V3_for_C4P.jpg

Two objectives are:

1.  A 360-degree view of constituents is important for PAWS to be able
to (1) fully understand the depth and breadth of constituent engagement; (2) accurately 
acknowledge the various aspects of support provided
by individuals; and (3) encourage, invite and inspire further engagement across PAWS'
various programs and opportunities to extend involvement in and support for PAWS mission.

2.  PAWS is increasingly interested in using data to better understand,
measure, and tune their operating processes.  Each study requires harversting
and wrangling data from one or more sources before any analyis can be done.  Having
data from each system regularly extracted and prepped (cleaned, matched, etc) for
analysis would speed such projects as they arise and directly support repeated
analyses over time.  

## Systems View - Summary

PAWS uses multiple **Operational Systems** to support its various operating needs.

    Salesforce - Fund raising
    Volgistics - Volunteer management 
    Petpoint - Animal management
    ClinicHQ - medical records for clinic patients (animals)
    iContact - email marketing
    Trello - workflow management
    (there are more... just not pertinent to our initial work)
    
Information on PAWS constituents is spread across these various systems.
Often the same constituent shows up in multiple systems 
with no guarantee as to how consistently they are represented 
(i.e. name, address, email, etc could be different, misspelled, or of 
different vintage - pre/post marriage, house move, etc).   Sometimes a constituent shows
up on only one system.   All constituents are important.

Each of these **Operational Systems** is ideally suited to what it does.  There is not 
a single system that can meet all various operating needs.  Thus we are in a
**multi-system** situation. 

## Envisioned Repositories
1. Salesforce's built-for purpose is as a constituent management system.  PAWS should use it in this
way.
Namely, all aspects of a constituent's relationship with PAWS should be **visible** in Salesforce to
the extent that such information helps to comprehend the 360-degree relationship (while **not** 
strictly duplicating **all** information in the various other Operational Systems).

2. It seems like a "Data Lake" would be valuable to hold detail information from all Operational Systems in
a way that makes it readily available for ongoing analysis.   This would be used by data scientists
to develop analyses and perhaps by PAWS staff running pre-developed scripts to update existing
analyses.  This would not be an end-user reference system.   End-user access is via the Operational Systems, with Salesforce focused on constituent information. 
  
## Use Cases
### Use Case: PAWS Staff Member or Administrative Volunteeer
- PAWS could pull up a constituent
in Salesforce and see thier contact information, their donation activity,
their volunteer activity, their adoption and fostering activity,
and their clinic visit activity - all at an appropriate level of
detail.  
- From this single review of their **Contact** record in Salesforce, the user 
can assess the relationship.   
- They can go deeper in Salesforce for Donation Info and can 
look at other Operational systems for extended detail.  
- Where possible, hyperlinking to 
other Operational systems should be included in Salesforce to ease finding more details information.

### Use Case: Data Scientist
- The data scientist and PAWS engage on the analysis needed
- The data scientist inspects the Data Lake for relevant data for the study at hand based upon source Operational
systems and analysis required
- If the data is not present, a project is initiated to identify, gather, and include such data in
the Data Lake
- If data is present, the Data Scientist uses Python, R, or other tools of choice to extract data
and perform analysis

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

Donations happen every day.   Volunteers work shifts every day.   Animals are fostered and adopted out every day.
At given intervals, PAWS staff or an empowered volunteer will 




