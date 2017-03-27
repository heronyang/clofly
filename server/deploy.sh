#!/bin/sh
docker build -t clofly-server .
docker run -d -p 80:80 -e "HOME=/root" -v $HOME/.aws:/root/.aws clofly-server
