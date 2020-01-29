Install docker
    https://docs.docker.com/install

run:  
`docker build -t ngnix_paws_image .`
`docker run --rm -it -p 5555:5555 ngnix_paws_image`


API:  
run http GET request like:    
- http://localhost:5555/listFiles
- http://localhost:5555/file/{fileName}
- http://localhost:5555/executeScript/{scriptName}
- http://localhost:5555/allFiles

public IP (use only for dummy data):  
replace http://localhost with - http://paws-data-pipeline.team-machine.phl.io . 
  
  
private IP (can use after added to ZeroTier):    
replace http://localhost with - http://10.147.20.146
