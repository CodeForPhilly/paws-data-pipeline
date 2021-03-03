# Getting Started

#### All of our code is in containers
- Install Docker - `https://docs.docker.com/install`  
- Install Docker Compose - `https://docs.docker.com/compose/install/`      

## Running everything (server and client)

- navigate to src directory `cd .../PAWS-DATA-PIPELINE/src`
- docker compose `docker-compose up`
- access the client going to `http://localhost:3000`

## Running just the client (front-end)

- navigate to src directory `cd .../PAWS-DATA-PIPELINE/src/client`
- set the PAWS_API_HOST=localhost or your ip
- docker compose `docker-compose up`
- access the client going to `http://localhost:3000`

## Running just the server (back-end)

- navigate to src directory `cd .../PAWS-DATA-PIPELINE/src/server`
- docker compose `docker-compose up`