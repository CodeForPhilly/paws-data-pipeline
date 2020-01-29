Install docker
    https://docs.docker.com/install

run:  
`docker build -t ngnix_paws_image .`
`docker run --rm -it -p 5555:5555 ngnix_paws_image`


API:  
run http GET request like:    
- http://localhost:5555
- http://localhost:5555/file/{fileName}
- http://localhost:5555/executeScript/{scriptName}
- http://localhost:5555/allFiles

public IP (use only for dummy data):  
replace http://localhost with - http://paws-data-pipeline.team-machine.phl.io . 
  
  
private IP (can use after added to ZeroTier):    
replace http://localhost with - http://10.147.20.146

If you signed the confidentiality agreement document and want access to the server, please download zeroTier software (https://www.zerotier.com/), create an account online, sign in, and then let Uri know on Slack. He’ll send you the id of the network and then you need to send him your node ID; then you can use the api in the private server
