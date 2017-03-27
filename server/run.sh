#!/bin/sh
uwsgi --http-socket :80 --processes 5 --master --enable-threads --wsgi-file uwsgi_server.py
