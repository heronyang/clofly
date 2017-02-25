#! /bin/bash

#Docker Engine Installation
sudo apt-get update

sudo apt-get install -y --no-install-recommends \
    linux-image-extra-$(uname -r) \
    linux-image-extra-virtual

sudo apt-get install -y --no-install-recommends \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common


curl -fsSL https://apt.dockerproject.org/gpg | sudo apt-key add -

sudo add-apt-repository \
       "deb https://apt.dockerproject.org/repo/ \
       ubuntu-$(lsb_release -cs) \
       main"

sudo apt-get update
sudo apt-get -y install docker-engine

#Docker-compose Installation, MUST be under root
#run "sudo -i" to run under root
curl -L "https://github.com/docker/compose/releases/download/1.11.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

