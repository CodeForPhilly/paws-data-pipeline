rm -rf src
tar -xzvf src.tar.gz
cd src
docker image build -t paws-data-pipeline .
docker container kill pdp
docker container rm pdp
docker container run --publish 5000:5555 --name pdp -d paws-data-pipeline