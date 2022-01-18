#!/bin/bash

# we may want to switch this to a script which logs output, etc?
echo "------------STARTING `date` ------------------"
set FLASK_APP=server/app.py
export FLASK_APP
source bin/export_secrets.sh
# This abomination ensures that the PG server has finished its restart cycle
echo "SLEEPING.. WAITING FOR DB"; sleep 5; echo "WAKING"; alembic upgrade head; alembic current; echo "DB SETUP";
#; python -m flask run --host=0.0.0.0 --no-reload

# --no-reload prevents Flask restart, which usually happens in middle of create_base_users()
#TODO: SECURITY - ensure we are not running in debug mode in production
uwsgi --http-socket :5000 --plugin python38 --module wsgi:app --chdir /app --pythonpath . --processes 2 --threads 4 --master
