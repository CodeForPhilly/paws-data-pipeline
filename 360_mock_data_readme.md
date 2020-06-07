# Run mock data for 360

##Populate data:
1. run the project
2. clean your docker volumes in order to create a clean DB 
3. upload files located here `sample_data/360_mock_data` to the server using the UI
4. run execute
5. the DB should be populated with 3 matches
6. flow script located here: `src/scripts/flow_script_for_360_mock.py`

##API:
1. endpoints are located here: `src/server/common_api.py`
2. get salesforce contacts: `localhost:[port]/cotacts`
3. get 360 of a salesforce cotacts by id: `localhost:[port]/360/<salesforce_contact_id>` 

