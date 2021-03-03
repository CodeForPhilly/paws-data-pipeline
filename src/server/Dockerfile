FROM python:3.8

RUN apt-get update && apt-get install -y vim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update

RUN apt-get install -y python3-dev uwsgi uwsgi-src libcap-dev uwsgi-plugin-python3
RUN pip install --upgrade pip

COPY requirements.txt /

RUN pip install --no-cache-dir -r /requirements.txt

RUN export PYTHON=python3.8
RUN uwsgi --build-plugin "/usr/src/uwsgi/plugins/python python38"
RUN mv python38_plugin.so /usr/lib/uwsgi/plugins/python38_plugin.so
RUN chmod 666 /usr/lib/uwsgi/plugins/python38_plugin.so

COPY . .

RUN mkdir /app/static \
    /app/static/raw_data \
    /app/static/raw_data/current \
    /app/static/output \
    /app/static/output/reports \
    /app/static/logs \
    /app/static/zipped

RUN [ ! -f /app/static/logs/last_execution.json ] && printf {} > /app/static/logs/last_execution.json

RUN chmod -R 777 /app/static

COPY . /paws-data-pipeline/server

RUN chmod 777 /paws-data-pipeline/server
# RUN ufw allow 5000
WORKDIR /app

# --uid uwsgi
CMD uwsgi --http-socket :5000 --plugin python38 --module wsgi:app --chdir /app --pythonpath .
# we may want to switch this to a script which logs output, etc?

RUN set FLASK_APP=server/app.py
RUN export FLASK_APP

# This abomination ensures that the PG server has finished its restart cycle
CMD echo "SLEEPING 10"; sleep 10; echo "WAKING"; alembic upgrade head ; python -m flask run --host=0.0.0.0 --no-reload

# --no-reload prevents Flask restart, which usually happens in middle of create_base_users()
#TODO: SECURITY - ensure we are not running in debug mode in production
