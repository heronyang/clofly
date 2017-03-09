#!/bin/sh
# Ubuntu 16.04

sudo apt update

# install docker
echo checking if docker is installed...
if [ ! $(which docker) ]
    then
        echo installing docker...
        sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
        sudo apt-add-repository 'deb https://apt.dockerproject.org/repo ubuntu-xenial main'
        apt-cache policy docker-engine
        sudo apt install -y docker-engine
        sudo systemctl status docker
        sudo usermod -aG docker $(whoami)
fi

# install pip
echo checking if pip is installed...
if [ ! $(which pip) ]
    then
        echo installing pip...
        sudo apt install -y python-pip
fi
sudo pip install -r requirements.txt

# install uwsgi
echo checking if uwsgi is installed...
if [ ! $(which uwsgi) ]
    then
        echo installing uwsgi...
        sudo apt-get install libpcre3 libpcre3-dev
        sudo pip install uwsgi
fi
