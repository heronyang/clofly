# Dasf - Deploy a Scalable Function

## Abstract

In today's world, application developers spend high cost renting virtual machines to host their applications, and most of their machines are not being used efficiently. Therefore, we designed a simple FaaS architecture that serves multiple functions in distributed systems. The functions will only cost resources when there's a reuqest, which means there's no runtime cost if there's no request for a function.

## Structure

- **server**: backend cgi code for Dasf, once there's a request, the cgi program will pull out the function from database then execute it in a docker container
- **api**: api for users to upload/download their function code
- **www**: front end code for users to manage their function code online
- **db**: database that stores user function code
- **function**: demo function code for dasf users

## Run Server

    $ cd server
    $ ./simple-server.py

## Deploy Function

    $ cd function
    $ node ../api/dasf.js hello.js

## Demo

[![Demo](https://img.youtube.com/vi/xJNUvu2haE8/0.jpg)](https://www.youtube.com/watch?v=xJNUvu2haE8)
