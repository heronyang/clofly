#!/bin/sh
# Ubuntu 16.04

if [ ! -f uwsgi.ini ]; then
    echo "Not found: uwsgi.ini"
    exit
fi

if [ ! -f uwsgi.service ]; then
    echo "Not found: uwsgi.service"
    exit
fi

sudo apt update

# install docker
echo Checking if docker is installed...
if [ ! $(which docker) ]
    then
        echo Installing docker...
        sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
        sudo apt-add-repository 'deb https://apt.dockerproject.org/repo ubuntu-xenial main'
        sudo apt update
        apt-cache policy docker-engine
        sudo apt install -y docker-engine
        sudo usermod -aG docker $(whoami)
fi

# install pip
echo Checking if pip is installed...
if [ ! $(which pip) ]
    then
        echo Installing pip...
        sudo apt install -y python-pip
fi
sudo pip install -r requirements.txt

# install uwsgi
echo Checking if uwsgi is installed...
if [ ! $(which uwsgi) ]
    then
        echo Installing uwsgi...
        sudo apt-get install -y libpcre3 libpcre3-dev
        sudo apt-get install -y uwsgi
        sudo apt install -y uwsgi-plugin-python
fi

current_dir=$(pwd)
echo $current_dir
sudo cp uwsgi.ini /etc/uwsgi/apps-available/uwsgi.ini
cd /etc/uwsgi/apps-enabled/
sudo ln -s ../apps-available/uwsgi.ini
cd $current_dir

sudo service uwsgi start
