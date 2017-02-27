# FROM node:alpine
FROM node:slim

# Create app directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Bundle app source
COPY . /usr/src/app

# Install app dependencies
RUN npm install
RUN node install-user-dependencies.js

EXPOSE 8080
CMD [ "npm", "start" ]
