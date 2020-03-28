# Getting into Chris's Salesforce Trailhead Sandbox

Two years ago I mocked up a bunch of stuff in a Salesforce training (Trailhead) instance.   They lasted 30 days back then.  So it's gone. My purpose was to see how non-SFDC data from other PAWS systems can be imported and associated with constituents (Salesforce Contacts) in SFDC.   Call it a Proof-of-Concept.  

I started another sandbox up a few months ago, and reloaded some of the data I used back then.  I also re-applied a number of customizations / configurations (although I did not take very good notes back then!).   

This gets you into that sandbox.   

The Non-Profit Success Pack (NPSP) is a set of Salesforce customizations intended to better serve Non-Profits.  
Installation of that seems to be 50/50 in this sandbox (which is all done in an automated fashion by SFDC automation), but it serves the purpose until we revive the Saleforce thread of this project and spend quality time with Weston getting a correct standbox in place.

The rest of this is showing the results of my proof-of-concept this time around.  
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

Pick the Non Profit Success Pack NPSP - the one in the middle (it's the one with the Lightning Experience.. .cooler)

![Pic5](https://github.com/CodeForPhilly/paws-data-pipeline/blob/cck-doc/documentation/documentation-images/SF-Pic5)

This is a two part step.   First click on the Contacts tab at the top.   That should bring up recently used Contacts.  If not, click around to bring up recent contacts.  It should be an option under the Contacts tab if you hover or click for the pull-down menu.

Then click on our buddy Aaron.   Fake name and address

![Pic6](https://github.com/CodeForPhilly/paws-data-pipeline/blob/cck-doc/documentation/documentation-images/SF-Pic6)

This is Aaron's contact record.  Note two two "Related" pieces of information.   Volunteer info especially.  

In PAWS' real Salesforce instance, you'd see a ton of valuable info, including donation history, addresses, family relationships, etc.  

![Pic7](https://github.com/CodeForPhilly/paws-data-pipeline/blob/cck-doc/documentation/documentation-images/SF-Pic7)

If you hover over Volunteer Hours, it will pop up a list (it's a subset) of the shifts he's worked.   These are Volunteer Shift instances which I pulled from REAL Volgistics data (but just associated it with "Aaron").    There is some background work to do be done to set up the shift types.   But it can be done once and in the very rare instances where a new shift shows up we can have a maintenance step to load the new Volunteer Shifts (and if needed Volunteer Campaigns). 

![Pic8](https://github.com/CodeForPhilly/paws-data-pipeline/blob/cck-doc/documentation/documentation-images/SF-Pic8)

If you go back and scroll around the Contact record, you'll see all sorts of good info.  Donation History (which I haven't loaded any of), and the Volunteer info is at the bottom.   This is a POC to show what it might look like for PAWS to see not only donation info but also Volunteer activity.   And we can add Animals to this as well.  Weston has a mock-up of that done, although he doesn't have the Volunteer hours.   We can pull this together over time to get a real solid POC.   

I loaded all data via file import wizard available in Salesforce.  API in and out of this Saleforce instance also works.  It's a full developer edition.  I set up the key etc and proved connection via Python.  That code is in the SFDC-Playground folder

There's also a bit of Saleforce screen and form modification I did to pull the Volunteer info in.   Most of it happened automatically when I did it two years ago.  Not sure of the differences. 
