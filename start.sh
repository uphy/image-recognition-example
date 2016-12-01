#!/bin/sh

WORKDIR=$(pwd)/work
IMAGE_NAME=imagerecognition
CONTAINER_NAME=imagerecognition_container

docker build -f Dockerfile -t $IMAGE_NAME:latest .
docker rm -f $CONTAINER_NAME > /dev/null 2>&1 
#docker run -it --name $CONTAINER_NAME -d -p 8888:8888 -v $WORKDIR:/work $IMAGE_NAME /bin/bash -c "jupyter notebook --port=8888 --ip=0.0.0.0"
docker run --name $CONTAINER_NAME -d -p 5000:5000 -p 8888:8888 -v $WORKDIR:/work $IMAGE_NAME
