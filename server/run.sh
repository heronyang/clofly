#!/bin/bash
sudo uwsgi --http :80 --processes 5 --master --enable-threads --wsgi-file uwsgi_server.py
