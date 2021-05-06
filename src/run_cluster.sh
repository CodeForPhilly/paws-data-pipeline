#  Creates and runs PDP on a kind-based clauster
#  If running on Windows, run on Bash (e.g., Git Bash) or change file ext from .sh to .cmd
#     .cmd works the same but you'll see echo lines twice

echo " "; echo ">>>>>>>>>>>>>>>>> Creating cluster. Now's a good time to go get coffee >>>>>>>>>>>>>>>>>"
kind create cluster

# Assumes kustomization.yaml lives in server/secets
echo " "; echo ">>>>>>>>>>>>>>>>> Create and add secrets to k8s environment >>>>>>>>>>>>>>>>>"
kubectl apply -k server/secrets 

echo " "; echo ">>>>>>>>>>>>>>>>>                 Build images             >>>>>>>>>>>>>>>>>"
docker-compose build

# So pods, specifically 'wait_for', have read access to API
echo " "; echo ">>>>>>>>>>>>>>>>>     Give pods access to k8s API         >>>>>>>>>>>>>>>>>"
kubectl create role pod-reader --verb=get --verb=list --verb=watch --resource=pods,services,deployments
kubectl create rolebinding default-pod-reader --role=pod-reader --serviceaccount=default:default --namespace=default

echo " "; echo ">>>>>>>>>>>>>>>>>     Tag and push client container image   >>>>>>>>>>>>>>>>>"
docker tag src_client localhost:5000/src-client:latest 
kind load docker-image localhost:5000/src-client:latest

echo " "; echo ">>>>>>>>>>>>>>>>> Tag and push server container image      >>>>>>>>>>>>>>>>>"
docker tag src_server localhost:5000/src-server:latest 
kind load docker-image localhost:5000/src-server:latest

echo " "; echo ">>>>>>>>>>>>>>>>> Apply k8s deployment files to launch containers  >>>>>>>>>>>>>>>>>"
kubectl apply -f k8s_conf

echo " "; echo ">>>>>>>>>>>>>>>>> Wait 20s in hopes that client service/container is live  >>>>>>>>>>>>>>>>>"
sleep 20

echo " "; echo ">>>>>>>>>>>>>>>>> Forwarding port 80 from cluster to localhost     >>>>>>>>>>>>>>>>>"
echo "'>>>>>>>>>>>>>>>>> Forwarding...' means it's working and will forward until ^C "
echo ">>>>>>>>>>>>>>>>>  To restart port-forwarding, 'kubectl port-forward service/client 80:80     '"
kubectl port-forward service/client 80:80        
echo " "; echo ">>>>>>>>>>>>>>>>> ^- Failed? Try running 'kubectl port-forward service/client 80:80' >>>>>>>>>>>>>>>>>"