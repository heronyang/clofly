# ![Clofly](/icon/icon-s.jpg?raw=true "Clofly")

A Scalable Serverless Service

## Abstract

In cloud computing services, the unit that service providers offer had moved from large instances to smaller computation units like docker containers. In 2016, Function as a Service (FaaS), represented by AWS Lambda, Google Cloud Functions, and Microsoft Azure Functions, was introduced as they allow users to upload functions without configuring or maintaining any cloud machine.

Although a variety of developer tools are written by open communities, limited discussion of the implementation of such service is found. We are currently developing a serverless service called Clofly, which behaves like AWS Lambda but the targeted users are totally different. We will be focusing on lowering the cost for developers in deploying their code as they don’t have to configure the servers at all, and their codes will be automatically deployed after one-line Clofly command. Scalability is the fundamental design principle while we are developing Clofly, and we believe this service can make the cloud machine be used in a much more efficient way.

## Structure

- **server**: uwsgi server code
- **api**: RESTFul api for our tools to interact with the database
- **cli**: command line interface for users to deploy and manage their function code
- **function**: demo function code for Clofly users

## Prerequisite for Local Machine

- **Docker**: v1.12.6
- **Python**: v2.7 with `pip` installed
- **node.js**: v6.9.5 with `npm` installed 

## Run Server

    $ cd server
    $ ./run.sh

## Deploy Function

    $ cd function/hello
    $ clofly start hello.js

## Demo

[![Demo](https://img.youtube.com/vi/JqEliUz-NzU/0.jpg)](https://www.youtube.com/watch?v=JqEliUz-NzU)

For developers (server behavior step-by-step):

[![Demo](https://img.youtube.com/vi/G2oxQYaj7zU/0.jpg)](https://www.youtube.com/watch?v=G2oxQYaj7zU)
