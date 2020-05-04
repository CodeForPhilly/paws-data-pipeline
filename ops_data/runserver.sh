#!/bin/bash
echo "Making sure DB is listening one last time before we do anything"
# Yeah, not a GREAT way to do it
sleep 10
cd /paws-data-pipeline/
echo "Importing database data"
python load_paws_data.py
echo "Loading API app"
python ./src/server/app.py
