#!/bin/bash

#sudo apt-get update
echo checking if Nginx is installed...
if [ ! $(which nginx) ]
	then
        echo Installing Nginx...
		sudo apt-get install nginx
fi
echo checking if uwsgi is installed...
if [ ! $(which uwsgi) ]
    then
        echo installing uwsgi...
        sudo apt-get install uwsgi
fi

root_user=$(whoami)
current_dir=$(pwd)
echo $current_dir

sudo cp uwsgi_config.ini /etc/uwsgi/sites-available/uwsgi_config.ini
cd /etc/uwsgi/sites-enable
sudo ln -s ../apps-available/uwsgi_config.ini
cd $current_dir
sudo cp default /etc/nginx/sites-available/default

sudo service nginx restart
sudo service uwsgi restart


