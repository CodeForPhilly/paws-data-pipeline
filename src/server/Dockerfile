FROM python:3.10.9-bullseye

RUN apt-get update && apt-get install -y vim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update

RUN apt-get install -y python3-dev uwsgi uwsgi-src libcap-dev uwsgi-plugin-python3
RUN pip install --upgrade pip

COPY requirements.txt /

RUN pip install --no-cache-dir -r /requirements.txt

RUN export PYTHON=python3.10
RUN uwsgi --build-plugin "/usr/src/uwsgi/plugins/python python310"
RUN mv python310_plugin.so /usr/lib/uwsgi/plugins/python310_plugin.so
RUN chmod 666 /usr/lib/uwsgi/plugins/python310_plugin.so

COPY . .

RUN mkdir /app/static \
    /app/static/raw_data \
    /app/static/logs \
    /app/static/zipped

RUN [ ! -f /app/static/logs/last_execution.json ] && printf {} > /app/static/logs/last_execution.json

RUN chmod -R 777 /app/static

RUN chmod +x  bin/startServer.sh
# RUN ufw allow 5000
WORKDIR /app

RUN useradd -m pawsapp
RUN mkdir -p  /app/.pytest_cache/v/cache
RUN chown -R pawsapp:pawsapp /app/.pytest_cache/v/cache
USER pawsapp

CMD bin/startServer.sh
#>> start.log 2>&1