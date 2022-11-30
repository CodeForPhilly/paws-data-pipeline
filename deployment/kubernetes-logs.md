# Kubernetes logs

Database logs are visible by attaching to paws-datapipeline-db and viewing `/var/lib/postgresql/data/log/`

Since Kubernetes performs liveness tests, there are a lot of test lines in the logs which you'll want to filter out

* On paws-datapipeline-server, filter on "that don't match" `/api/user/test`
* On paws-datapipeline-client, filter on "that don't match" `GET /`
