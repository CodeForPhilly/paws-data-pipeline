Run the PAWS data pipeline locally
---------------------------------------
#### Run local - when debugging
- Install dependencies: `pip install -r requirements.txt`
- Run docker compose (as explained below) in order to have the postgres docker running.
- Set environment variable: `export IS_LOCAL=True`
- If your docker IP is not localhost or you want to run postgres with a different user name etc  
  - Set environment variable: `export LOCAL_DB_IP=postgresql://postgres:thispasswordisverysecure@[your_docker_ip]/postgres`
  - Working directory should be: `...paws-data-pipeline/src`
- Set environment variable: `export FLASK_PORT=3333` we need it to be a different port then the one in the docker-compose
- Run python3 app.py
- Download the file `secrets.py` from the teams dropbox and place it under `src/server`.
#### Run docker - before pushing your code
- Install docker - `https://docs.docker.com/install`  

_Docker Compose instructions_  
- Install Docker Compose - `https://docs.docker.com/compose/install/`      
- Most package managers have it as `docker-compose` and it's largely just a shell script.    
- `docker compose up -d` to bring up the database and the server.

#### Finally - Run The UI on http://localhost:3000

---------------------------------------
Deploy
---------------------------------------
- `docker-compose` should use the profile flag `production-only`. i.e: `docker-compose --profile production-only up
` and `docker-compose --profile production-only build`

TBD   

--------------------------
Troubleshooting
---------------------------------------
See the [Troubleshooting page](https://github.com/CodeForPhilly/paws-data-pipeline/wiki/Troubleshooting) at the GitHub wiki. 