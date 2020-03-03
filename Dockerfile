FROM tiangolo/uwsgi-nginx-flask:python3.7

ENV LISTEN_PORT=5555
EXPOSE 5555

# Indicate where uwsgi.ini lives
ENV UWSGI_INI uwsgi.ini

# Set the folder where uwsgi looks for the app
WORKDIR /paws-data-pipeline/

# Copy the app contents to the image
COPY . /paws-data-pipeline/
RUN chmod 777 /paws-data-pipeline
RUN chmod 777 -R /paws-data-pipeline/output_data
COPY src/api_server/static/ /app/static/
RUN chmod -R 777 /app/static

RUN apt-get update
RUN apt-get install -y sqlite3 libsqlite3-dev

# If you have additional requirements beyond Flask (which is included in the
# base image), generate a requirements.txt file with pip freeze and uncomment
# the next three lines.

COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt