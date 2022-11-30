# Kubernetes Setup

### Introduction

I've started a Kubernetes (k8s) setup in the 'k8sify' fork, with the config files in the k8s\_conf directory. I'm using [KinD](https://kind.sigs.k8s.io/docs/user/quick-start/) (Kubernetes in Docker) so the cluster setup may differ but once running, kubectl should behave the same across any provider.

**Welcome to Kubernetes!**

![](https://camo.githubusercontent.com/1c4f97f1c816dafa5bb5e315c4612969fca8b2cbdd0ad3207e3d0812b1e49ce6/68747470733a2f2f65787465726e616c2d707265766965772e726564642e69742f592d474d41307556556d4133634639424e4b3554774778344346463732765f38736c4a374543584a6236342e6a70673f6175746f3d7765627026733d65363065353936363234303763353162373939333938663339346135303837643239303637313265)

Some light reading: [https://kubernetes.io/docs/concepts/](https://kubernetes.io/docs/concepts/)\
FYI, The Kubernetes and Docker extensions for VSCode make all of this easier.

### Create cluster

Run the [`kind_w_reg.sh`](https://github.com/CodeForPhilly/paws-data-pipeline/blob/master/src/k8s\_conf/kind\_w\_reg.sh) script to create a Kind cluster with a local Docker image registry/storage. \[1]\
N.B: You will want to stop the registry container when running locally to prevent a conflict on port 5000

### Tag your Docker images

Add the following tags to the appropriate existing Docker images:

* `localhost:5000/postgres:11.3-alpine`
* `localhost:5000/src-client:latest`
* `localhost:5000/src-server:latest`

_e.g.,_ `docker tag src_client localhost:5000/src-client:latest` (the VSCode Docker extension is your friend)

### Push each image to the local registry

`docker push <tag>` _e.g.,_ `docker push localhost:5000/src-server:latest` (Or use Docker extension)

### Deploy the images

From the src directory, `kubectl -f k8s_conf` will execute ('apply') all the yaml files in the k8s\_conf directory. You can specify an individual file, too.

Wait a minute or so and then run `kubectl get pods` to see the status of your running pods. You should see three with status RUNNING. Though they are happily running, they can only be accessed from inside the cluster.

### Make client available for access

`kubectl port-forward service/client 3000:3000` will make the PDP client available at `localhost:3000`

### Notes

\[1] Registry setup: [https://docs.docker.com/registry/deploying/](https://docs.docker.com/registry/deploying/)

(This was originally at [https://github.com/c-simpson/paws-data-pipeline/wiki/Kubernetes-setup](https://github.com/c-simpson/paws-data-pipeline/wiki/Kubernetes-setup))
