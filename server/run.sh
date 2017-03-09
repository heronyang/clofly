#!/bin/bash
sudo uwsgi --http :80 --master --enable-threads --wsgi-file uwsgi_server.py
