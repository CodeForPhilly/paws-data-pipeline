kind create cluster

kubectl apply -k server/secrets 

docker-compose build


docker tag src_client localhost:5000/src-client:latest 
kind load docker-image localhost:5000/src-client:latest


docker tag src_server localhost:5000/src-server:latest 
kind load docker-image localhost:5000/src-server:latest


kubectl apply -f k8s_conf

kubectl port-forward service/client 80:80        