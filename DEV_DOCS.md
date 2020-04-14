---------------------------------------
Install docker
---------------------------------------
    https://docs.docker.com/install

---------------------------------------
To run the PAWS data pipeline locally
---------------------------------------
_Non-compose instructions_

Build the Docker image, preparing it for execution:  `docker build -t paws-data-pipeline .`

Execute: `docker run --publish 5000:5555 --name pdp -d paws-data-pipeline`


_Compose instructions_

First, install Docker Compose. Most package managers have it as `docker-compose` and it's largely just a shell script.

`docker compose -d up` to bring up the database and the server.

---------------------------------------  
Using Private Network with Production:
---------------------------------------
Private IP (can use after added to ZeroTier):    
then go to: http://10.147.20.146:5000/

If you signed the confidentiality agreement document and want access to the server, please download zeroTier software (https://www.zerotier.com/), create an account online, sign in, and then let Uri know on Slack. He’ll send you the id of the network and then you need to send him your node ID; then you can use the api in the private server

---------------------------------------
To deploy
---------------------------------------
From local machine:
1. ZIP the project folder: `tar -czvf src.tar.gz src`
2. SCP the project to the server: `scp src.tar.gz [usrmname]@paws-data-pipeline.team-machine.phl.io:/home/[usrmname]/paws-data-pipeline`
3. SSH into the server: `ssh [usrmname]@paws-data-pipeline.team-machine.phl.io`

In server:
1. `cd paws-data-pipeline`
2. run `sh run.sh`
