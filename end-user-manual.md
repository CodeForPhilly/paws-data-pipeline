# User Manual

## What does the PAWS data pipeline do?

The pipeline matches constituent records from SalesForce, ShelterLuv and Volgistics to create a comprehensive list of all of PAWS’ constituents. Once matched, the pipeline 

1. sends constituent records back to SalesForce with updated information, 
2. provides the data needed to execute the RFME score in SalesForce, and 
3. creates 2 exports: 

    a. Possible duplicates for PAWS staff to review  
    b. New constituents to be added to SalesForce

### What data is used?

The data pipeline pulls the following information from the sources below, combines them with SalesForce data, and presents them for consumption in SalesForce:
Volgistics:

- Volgistics ID
- First Volunteer Date
- Last Volunteer Date

ShelterLuv:

- ShelterLuv ID
- Foster Start Date
- Foster End Date

### How are records matched? 

Every time the pipeline runs, it only uses currently available information; that is, it does not look at previous matching runs. At each run, it matches names, emails, and phone number data from each source against the other sources, creating pairs of matches. For instance, Jane Doe in Salesforce matches Jane Doe in Volgistics on name; but Jane Doe in Volgistics matches Janet Doe in ShelterLuv based on last name and phone number. In this case, Jane Doe in Salesforce and Volgistics are considered the same constituent as Janet Doe in ShelterLuv.

### What is the RFME score?

RFME stands for Recency, Frequency, Monetary Value, and Engagement, and is a score that helps PAWS staff focus outreach efforts. The calculation for this score is done in SalesForce, and was programmed by a volunteer developer working on the PAWS data pipeline project. However, it can be changed by PAWS as needed without relying on additional development resources. 

## How do I run the matching algorithm?

The matching algorithm runs on a schedule, and does not have the option for manual trigger. Prior to running the matching logic, the pipeline needs the most recent data from all 3 sources. The connection to SalesForce and ShelterLuv is automatic, so it always accesses the most recent data. However, data from Volgistics needs to be uploaded manually by a PAWS staff member prior to the scheduled execution of the matching logic. Follow the steps below to upload data from Volgistics: 

### 1. Log into the Pipeline 

Log in to the pipeline here: https://test.pawsdp.org/ using your PAWS PDP account. 

**What if I don’t have an account?** New users can be created by a PAWS admin user (contact PAWS staff to help with this). 
**What if I forgot my password?** A PAWS admin user can also reset passwords for other users. Contact PAWS staff for assistance.

### 2. Download data from Volgistics to your computer

Log in to Volgistics, go to Print -> Table Style Reports -> Excel Spreadsheet -> "All volunteer information (stock)"
When the report is done, an email will appear in the Volgistics Mailbox with the subject "All volunteer information (stock)"; clicking on this message will save the excel file to your computer

### 3. Upload volunteer data into the pipeline

Go to the pipeline website (https://test.pawsdp.org/), log in as admin, go to "Admin" tab, select the Volgistics file from your Downloads, and click Upload
Upload can take a few minutes; when the upload is done, there is no immediate feedback; navigate to a different tab and then back to the Admin tab to see if the "Last Updated" date was refreshed

You are done! The automated process will take it from here!

## What updated data can I see in SalesForce?

After the data is uploaded, the pipeline will run at its next scheduled time and will pick up this Volgistics data, together with the latest SalesForce and ShelterLuv data. It will then match records across these 3 sources. When it’s done, updated data will appear in SalesForce in each constituent’s record under the following fields: 

- Volgistics ID
- ShelterLuv ID
- First Volunteer Date
- Last Volunteer Date
- Foster Start Date
- Foster End Date
- Foster Status
- RFME score 

## How do I see the exports? 
To help with deduplication and ensure SalesForce remains the source of truth for PAWS, the pipeline provides (after each run), two exports for PAWS staff:

### Duplicates

If the pipeline identifies duplicate constituents (ie, individuals who have multiple SalesForce contact IDs), a list will be generated for PAWS staff to review. This list can be found at https://test.pawsdp.org/. 

- If, upon review, PAWS staff decide that these records are true duplicates, PAWS staff will need to use SalesForce tools to de-dupe and merge contacts. Once the duplicate record disappears from SalesForce, the data pipeline will no longer identify it as a duplicate. 
- If the duplicated individuals were incorrectly identified as duplicates by the automated process, PAWS staff should seek to add identifying information to the SalesForce record (e.g. email address, phone number) or correct any spelling, where applicable. If the duplication persists in future runs despite these changes, it can be ignored. 

### New SalesForce contacts

If the pipeline identifies contacts that are volunteers, fosters or adopters, but who are not in SalesForce, it will produce a list of those contacts, which can also be found at https://test.pawsdp.org/. These records will need to be manually evaluated by PAWS staff, and a contact will need to be manually created in SalesForce for them. Once in SalesForce, the pipeline will match them to their Volgistics and ShelterLuv information at the next run. 

