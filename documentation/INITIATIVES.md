
## Overall Description

PAWS uses multiple software (cloud-based) systems to support its various operating needs.  Information
on PAWS constituents is spread across these **Operational Systems** with varying levels of
consistency (/inconsistency) in how they are represented.

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

##Envisioned Repositories
1. Salesforce's built-for purpose is as a constituent management system.  PAWS should use it in this
way.
Namely, all aspects of a constituent's relationship with PAWS should be **visible** in Salesforce to
the extent that such information helps to comprehend the 360-degree relationship (while **not** 
strictly duplicating **all** information in the various other Operational Systems).

2. It seems like a "Data Lake" would be valuable to hold detail information from all Operational Systems in
a way that makes it readily available for ongoing analysis.   This would be used by data scientists
to develop analyses and perhaps by PAWS staff running pre-developed scripts to update existing
analyses.  This would not be an end-user reference system.   That reference would be Salesforce along 
with the Operational Systems.   
  
> Use Case - PAWS Staff Member or Administrative Volunteeer
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

> Use Case - Data Scientist
- The data scientist and PAWS engage on the analysis needed
- The data scientist inspects the Data Lake for relevant data for the study at hand based upon source Operational
systems and analysis required
- If the data is not present, a project is initiated to identify, gather, and include such data in
the Data Lake
- If data is present, the Data Scientist uses Python, R, or other tools of choice to extract data
and perform analysis

(MORE TO COME....  UPLOADING IT TO CHECK FORMATTING)




