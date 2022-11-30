# Local Setup

### Run the PAWS data pipeline locally

**Run local - when debugging**

* Install dependencies: `pip install -r requirements.txt`
* Run docker compose (as explained below) in order to have the postgres docker running.
* Set environment variable: `export IS_LOCAL=True`
* If your docker IP is not localhost or you want to run postgres with a different user name etc
  * Set environment variable: `export LOCAL_DB_IP=postgresql://postgres:thispasswordisverysecure@[your_docker_ip]/postgres`
* Working directory should be: `...paws-data-pipeline/src`
* Set environment variable: `export FLASK_PORT=3333` we need it to be a different port then the one in the docker-compose
* Run python3 app.py
* Download the file `secrets_dict.py` from the teams dropbox and place it under `src/server`.

**Run docker - before pushing your code**

* Install docker - `https://docs.docker.com/install`

_Docker Compose instructions_

* Install Docker Compose - `https://docs.docker.com/compose/install/`
* Most package managers have it as `docker-compose` and it's largely just a shell script.
* `docker-compose up -d` to bring up the application.
* Scheduler docker will not start. To run the scheduler, use profile flag `production-only` as explained in the Production Environment section.

**Finally - Run The UI on** [**http://localhost:80**](http://localhost/)

## Windows Setup

This guide contains steps to run the app locally for Windows users.​

### Configure git to handle line ending issues

* Before downloading the source code, run the following commands:

```
git config core.eol lf
git config core.autocrlf input
```

### Download the source code

* Navigate to local destination directory.
* Clone the repo - `> git clone https://github.com/CodeForPhilly/paws-data-pipeline`​

### Confirm correct line endings

* The above `> git config` commands should configure git to change line endings from CRLF to LF in the `clone` process, but to avoid trouble, double check that the following files have LF line endings:

```
src/server/bin/startServer.sh
src/server/bin/export_secrets.sh
src/server/secrets_dict.py
```

See [this](https://github.com/carrollsa/carrollsa\_public/blob/main/CRLFtoLF-VSC.md) gif for how to check line endings and change them, if necessary, in VSC.​

### Run the Docker container

* Run the Docker Desktop client locally
* Navigate to `../paws-data-pipeline/src`
* Build the container (do this every time you make a change to the code): `> docker-compose build`
* Run the container: `> docker-compose up`

The client should now be accessible at `http://localhost:80`.

Note - Changes made to the image files require removing volumes and rebuilding the container:

* `> docker-compose down-v`
* `> docker-compose build`
* `> docker-compose up`​

### Running the frontend

#### Configure package.json

* Windows requires different syntax for setting environment variables. As a result, the `package.json` file must be changed.

In `/src/client/package`, change:

```
"scripts": {
    "start": "IS_LOCAL=false react-scripts start",
    "start:local": "IS_LOCAL=true react-scripts start",
    ...
}
```

to

```
"scripts": {
  "start": "set IS_LOCAL=false && react-scripts start",
  "start:local": "set IS_LOCAL=true && react-scripts start",
  ...
}
```

#### Run the local client

* Navigate to `../paws-data-pipeline/src/client`
* Install dependencies locally - `> npm install`
* Run the client - `> npm run start`

The client should now be accessible at `http://localhost:3000`.​

#### Accessing the Docker API from the local client

The Docker container should expose an endpoint that the local client can access. You can test this in a browser while the container is running by navigating to `http://localhost:5000/api/user/test`. If you do not see `"OK from User Test @ ..."`, see [troubleshooting](https://github.com/CodeForPhilly/paws-data-pipeline/wiki/Troubleshooting#docker-api-unavailable).



### Production Environment

* `docker-compose` should use the profile flag `production-only`. i.e: `docker-compose --profile production-only up` and `docker-compose --profile production-only build`
