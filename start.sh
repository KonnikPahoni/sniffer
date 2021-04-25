#!/bin/sh

docker stop cryptosniffer_redis && docker container rm cryptosniffer_redis
docker run -v "$(pwd)/docker/redis-data":/data --name cryptosniffer_redis -p 6379:6379 -d redis redis-server --appendonly yes

docker stop cryptosniffer_postgres && docker container rm cryptosniffer_postgres
docker run --name cryptosniffer_postgres -p 5432:5432 -e POSTGRES_PASSWORD=password -e POSTGRES_USER=postgres -d postgres

docker stop cryptosniffer_celery && docker container rm cryptosniffer_celery
docker run --link cryptosniffer_redis -e CELERY_BROKER_URL="redis://redis:6379/0" --expose=6379 --name cryptosniffer_celery -d celery


docker stop cryptosniffer_app && docker container rm cryptosniffer_app
docker build -t cryptosniffer_app_image .
docker run --name cryptosniffer_app --network="host" -v "$(pwd)/docker":/var cryptosniffer_app_image