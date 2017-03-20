#!/bin/bash
sudo apt update
sudo apt install -y python-pip python-dev nginx
sudo pip install uwsgi flask
