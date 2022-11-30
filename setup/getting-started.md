# Getting Started

### Dependencies

Running Paws Data Pipeline locally requires the following:

* Python v3.8 or higher (for backend development) - Download [here](https://www.python.org/downloads/).
* Node (for frontend development) - Download [here](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm).
* Docker (v 20.10.21 or higher) - Download [here](https://docs.docker.com/get-docker/).
* docker-compose (v 2.12.2 or higher)
* Git - Download [here](https://git-scm.com/downloads). To troubleshoot, reference the documentation [here](https://git-scm.com/doc).
* libpq-dev (v 10.22 or higher)
* libc - (v 2.28 or higher)
* wsl2 (if using Windows Linux Subsystem)

### Suggested Extensions

* VSCode Docker extension - Download [here](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker).

Windows users, see our [wiki](https://github.com/CodeForPhilly/paws-data-pipeline/wiki/Windows-Setup) for alternate directions from this point.​

### Download the source code

* Navigate to local destination directory.
* Clone the repo - `$ git clone https://github.com/CodeForPhilly/paws-data-pipeline`​

### Run the Docker container

* Run the Docker Desktop client locally (\_review 4) (Mac) \[Linux directions will be provided by Cris]
* Navigate to `../paws-data-pipeline/src`
* Build the container (do this every time you make a change to the code): `$ docker-compose build`
* Run the container: `$ docker-compose up`

The client should now be accessible at `http://localhost:80`.

Note - Changes made to the image files require removing volumes and rebuilding the container:

* `$ docker-compose down -v`
* `$ docker-compose build`
* `$ docker-compose up`​

### Running the frontend

* Navigate to `../paws-data-pipeline/src/client`
* Install dependencies locally - `$ npm install`
* Run the client - `$ npm run start`

The client should now be accessible at `http://localhost:3000`.​

### Accessing the Docker API from the local client

The Docker container should expose an endpoint that the local client can access. You can test this in a browser while the container is running by navigating to `http://localhost:5000/api/user/test`. If you do not see `"OK from User Test @ ..."`, see [troubleshooting](https://github.com/CodeForPhilly/paws-data-pipeline/wiki/Troubleshooting#docker-api-unavailable).
