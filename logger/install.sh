#! /bin/bash

# Install Sentry server via docker
mkdir -p data/postgres

docker run \
  --detach \
  --name sentry-redis \
  redis:3.2-alpine

docker run \
  --detach \
  --name sentry-postgres \
  --env POSTGRES_PASSWORD=secret \
  --env POSTGRES_USER=sentry \
  postgres:9.5

docker-compose run --rm web upgrade
docker-compose up -d


