FROM tiangolo/uwsgi-nginx-flask:python3.7

ENV FLASK_APP api_server/api_app.py
ENV FLASK_RUN_HOST 0.0.0.0

# Indicate where uwsgi.ini lives
ENV UWSGI_INI uwsgi.ini

# Set the folder where uwsgi looks for the app
WORKDIR /paws-data-pipeline/

# Copy the app contents to the image
COPY . /paws-data-pipeline/
RUN chmod 777 /paws-data-pipeline
COPY api_server/static/ /app/static/
RUN mkdir /app/static/uploads
RUN mkdir /app/static/uploads/current
RUN mkdir /app/static/output
RUN mkdir /app/static/output/reports
RUN mkdir /app/static/logs
RUN chmod -R 777 /app/static

RUN apt-get update

# If you have additional requirements beyond Flask (which is included in the
# base image), generate a requirements.txt file with pip freeze and uncomment
# the next three lines.

COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt
CMD ["flask", "run"]