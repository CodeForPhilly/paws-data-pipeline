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
#### Run docker - before pushing your code
- Install docker - `https://docs.docker.com/install`  

_Docker Compose instructions_  
- Install Docker Compose - `https://docs.docker.com/compose/install/`      
- Most package managers have it as `docker-compose` and it's largely just a shell script.    
- `docker compose up -d` to bring up the database and the server.

#### Finally - Run The UI on http://localhost:3000
   
---------------------------------------  
Production Private Network:
---------------------------------------    
- Sign the confidentiality agreement with Chris or Karls.  
- Download zeroTier software -`https://www.zerotier.com/`  
- Create an account online.  
- Sign in and join the network `e5cd7a9e1c5330df`  
- Talk to Uri/Chris Alfano to approve your zeroTier node and send your node_id. 
- URL: `http://10.147.20.146:3000/` 
---------------------------------------
Deploy
---------------------------------------
From local machine:
1. SSH into the server: `ssh [usrmname]@paws-data-pipeline.team-machine.phl.io` 

In server:
1. access root
2. git clone `https://github.com/CodeForPhilly/paws-data-pipeline.git`
3. `cd paws-data-pipeline`
2. run `sh deploy_from_tar_docker-compose.sh`

--------------------------
Brutally clean all docker related items from your machine
--------------------------
  `docker stop $(docker ps -aq) && docker rm $(docker ps -aq) && docker network prune -f && docker rmi -f $(docker images --filter dangling=true -qa) && docker volume rm $(docker volume ls --filter dangling=true -q) && docker rmi -f $(docker images -qa)`
