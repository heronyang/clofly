FROM ubuntu:16.04

ADD . /clofly
WORKDIR /clofly

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install --assume-yes apt-utils

RUN apt-get install -y python python-pip
RUN pip install --upgrade pip

RUN pip install -r requirements.txt

RUN apt-get install -y libpcre3 libpcre3-dev
RUN apt-get install -y uwsgi uwsgi-plugin-python

RUN apt-get install -y curl
RUN curl -sL https://deb.nodesource.com/setup_7.x | bash
RUN apt-get install -y nodejs
RUN npm install -g `paste -s -d ' ' whitelist-npm-dependencies.txt`

EXPOSE 80

CMD ["./run.sh"]
ENV DEBIAN_FRONTEND teletype
