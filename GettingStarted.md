# Getting Started

#### All of our code is in containers
- Install Docker - `https://docs.docker.com/install`  
- Install Docker Compose - `https://docs.docker.com/compose/install/`      

## Running everything (server and client)
- navigate to src directory `cd .../PAWS-DATA-PIPELINE/src`
- docker compose `docker-compose up`
- access the client going to `http://localhost:3000`
## Running the client (front-end) locally
- navigate to src directory `cd .../PAWS-DATA-PIPELINE/src`
- docker compose `docker-compose run server`
- start the frontend with the proxy`npm run start:local`

## Running just server (back-end) locally
- navigate to src directory `cd .../PAWS-DATA-PIPELINE/src`
- set the PAWS_API_HOST=localhost or your ip in `docker-compose.yml`
- docker compose `docker-compose up` and stop the server