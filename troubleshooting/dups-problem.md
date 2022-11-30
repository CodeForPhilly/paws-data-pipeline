# Dups Problem

Why do they happen?

Salesforce:

* over 2k dups
* entered by different people into SF
* entered with different info (email, mail address, phone, etc)
* entered as part of another "household" (eg Jane Smith of "Jane Smith Household" and Jane Smith of "Jane Smith and John Doe Household")

Volgistics:

* 4 dups
* assume this happened as a result of a transition from one ID assignment convention to another, or because these volunteers took a longer break

ShelterLuv:

* 593 dups
* some are test entries (e.g. Firstname is a number, or "aaaa")
* imported as dups from PetPoint; entered as separate IDs in PetPoint when they adopted another animal, usually have different addresses too

What to do with them?

In SF, unclear which ID is "most recent", unless Contact IDs have some date/time info contained in them; we therefore cannot make an informed decision which entry to discard as outdated, so we need to keep them all and allow PAWS to mark outdated addresses. This may mean we have to store a separate table for contact info, where 1 contact can have multiple addresses, phone numbers, etc. Donation info should be summed across these dups In Volgistics, similar to SF, we should combine these entries; volunteer hours should be summed across these dups in ShelterLuv, similar to SF & Volgistics, we should combine entries; adopted animals should be aggregated across these dups combine dups based on First name + Last name combo; while there may be some people with identical names who are merged into 1 record this way, the percentage is small, and we can caution PAWS about this for MVP. However, PAWS needs to be able to correct this (either via an interface, or via one of us who goes in and manually edits)
