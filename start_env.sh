#! /bin/sh

sudo systemctl stop postgresql.service
sudo docker-compose up -d
source venv/bin/activate
export IS_LOCAL=True
export FLASK_PORT=3333
python src/app.py
