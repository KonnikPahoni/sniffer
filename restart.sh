#!/bin/sh

docker stop cryptosniffer_app && docker container rm cryptosniffer_app
docker build -t cryptosniffer_app_image .
docker run --name cryptosniffer_app --network="host" -v "$(pwd)/docker":/var cryptosniffer_app_image