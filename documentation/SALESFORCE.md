# Getting into Chris's Salesforce Trailhead Sandbox

Two years ago I mocked up a bunch of stuff in a Salesforce training (Trailhead) instance.   They lasted 30 days back then.  So it's gone.
My purpose was to see how non-SFDC data from other PAWS systems can be imported and associated with constituents (Salesforce Contacts) in SFDC.   Call it a Proof-of-Concept.  
The Non-Profit Success Pack (NPSP) is a set of Salesforce customizations intended to better serve Non-Profits.  
Installation of that seems to be 50/50 in this sandbox (which is all done in an automated fashion by SFDC automation), but it serves the purpose until we revive the Saleforce thread of this project and spend quality time with Weston getting a correct standbox in place.

The rest of this is showing the results of my proof-of-concept 
I have some screenshots here to help you get in and look around.  Follow along.   I don't think you can mess anything up but please try not to anyway.

Go to www.salesforce.com
sign in as chris@brave-fox-riktj8.com    Password is code1234

You will come to a screen like this:  

![Pic1](https://github.com/CodeForPhilly/paws-data-pipeline/blob/cck-doc/documentation/documentation-images/SF-pic-1)

Click on that rubics cube looking thing to bring up the app chooser

![Pic2](https://github.com/CodeForPhilly/paws-data-pipeline/blob/cck-doc/documentation/documentation-images/SF-Pic2)

Then pick View All   (click where circled)

![Pic3](https://github.com/CodeForPhilly/paws-data-pipeline/blob/cck-doc/documentation/documentation-images/SF-Pic3)

Scroll Down (by scrolling up if you use a mac)

![Pic4](https://github.com/CodeForPhilly/paws-data-pipeline/blob/cck-doc/documentation/documentation-images/SF-Pic4)

Pick the Non Profit Success Pack NPSP - the one in the middle (it's the one with the Lightening Experience.. .cooler)

![Pic5](https://github.com/CodeForPhilly/paws-data-pipeline/blob/cck-doc/documentation/documentation-images/SF-Pic5)

This is a two part step.   First click on the Contacts tab at the top.   That should bring up recently used Contacts.  If not, click around to bring up recent contacts.  It should be an option under the Contacts tab if you hover or click for the pull-down menu.

Then click on our buddy Aaron.   Fake name and address

![Pic6](https://github.com/CodeForPhilly/paws-data-pipeline/blob/cck-doc/documentation/documentation-images/SF-Pic6)

This is Aaron's contact record.  Note two two "Related" pieces of information.   Volunteer info especially.  

![Pic7](https://github.com/CodeForPhilly/paws-data-pipeline/blob/cck-doc/documentation/documentation-images/SF-Pic7)

If you hover over Volunteer Hours, it will pop up a list (it's a subset) of the shifts he's worked.   These are Volunteer Shift instances which I pulled from REAL Volgistics data (but just associated it with "Aaron").    There is some background work to do be done to set up the shift types.   But it can be done once and in the very rare instances where a new shift shows up we can have a maintenance step to load the new Volunteer Shifts (and if needed Volunteer Campaigns). 

![Pic8](https://github.com/CodeForPhilly/paws-data-pipeline/blob/cck-doc/documentation/documentation-images/SF-Pic8)

This should get you started.  Poke around.  
