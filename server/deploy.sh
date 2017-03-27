#!/bin/sh
docker build -t cloflyd .
docker run -p 80:80 -e "HOME=/root" -v $HOME/.aws:/root/.aws cloflyd
