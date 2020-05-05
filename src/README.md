---------------------------------------
Run the PAWS data pipeline locally
---------------------------------------
#### Run local - when debugging
- Install dependencies: `pip install -r requirements.txt`
- Run docker compose (as explained below) in order to have the postgres docker running.
- Set environment variable: `export IS_LOCAL=True`
- If your docker IP is not localhost or you want to run postgres with a different user name etc  
  - Set environment variable: `export LOCAL_DB_IP=postgresql://postgres:thispasswordisverysecure@[your_docker_ip]/postgres`
- Set environment variable: `export FLASK_PORT=3333` we need it to be a different port then the one in the docker-compose
- Run app.py
#### Run docker - before pushing your code
- Install docker - `https://docs.docker.com/install`  

_Compose instructions_  
- Install Docker Compose - `https://docs.docker.com/compose/install/`      
- Most package managers have it as `docker-compose` and it's largely just a shell script.    
- `docker compose up -d` to bring up the database and the server.

_Non-compose instructions_  (not being used anymore)  
- Build the Docker image, preparing it for execution:  `docker build -t paws-data-pipeline .`  
- Execute: `docker run --publish 5000:5555 --name pdp -d paws-data-pipeline`    
---------------------------------------  
Production Private Network:
---------------------------------------    
- Sign the confidentiality agreement with Chris or Karls.  
- Download zeroTier software -`https://www.zerotier.com/`  
- Create an account online.  
- Sign in and join the network `e5cd7a9e1c5330df`  
- Talk to Uri/Chris Alfano to approve your zeroTier node and send your node_id. 
- URL: `http://10.147.20.146:5000/` 
---------------------------------------
Deploy
---------------------------------------
From local machine:
1. ZIP the project folder: `tar -czvf src.tar.gz src`
2. SCP the project to the server: `scp src.tar.gz [usrmname]@paws-data-pipeline.team-machine.phl.io:/home/[usrmname]/paws-data-pipeline`
3. SSH into the server: `ssh [usrmname]@paws-data-pipeline.team-machine.phl.io`

In server:
1. `cd paws-data-pipeline`
2. run `sh deploy_from_tar_docker-compose.sh`
