#!/usr/bin/env python

import sys, os
import random
import time
import httplib
import boto3
from shutil import copyfile
from subprocess import check_output
from urllib2 import Request, urlopen, URLError, HTTPError
from socket import error as SocketError

NODEJS_TEMPLATE     = './node-template'
IMAGE_NAME_PREFIX   = 'clofly/nodejs-user-function-'
HEARTBEAT_PERIOD    = 0.01

class NodeFunctionManager():

    def __get_fid_dir(self, fid):
        return NODEJS_TEMPLATE + '-' + fid.replace('/', ',')

    def load(self, fid):

        # load requested function to disk
        print 'Loading function id: ' + fid

        # downlaod from database
        uf = self.__download_function(fid)

		# setup working directory
        fid_dir = self.__get_fid_dir(fid)
        return self.__setup_directory(fid_dir, uf)

    def __download_function(self, fid):

        db          = boto3.resource('dynamodb')
        table       = db.Table('user-function')
        response    = table.get_item( Key={ 'fid': fid })
        uf          = response['Item']['code']

        if not bool(uf):
            raise Exception('Function not found')

        return uf

    def __setup_directory(self, fid, uf):

        # temp directory name
        directory = self.__get_fid_dir(fid)

        # copy template folder to target folder
        self.__exec(['cp', '-r', NODEJS_TEMPLATE, directory])

        # load code
        uf_filepath = directory + '/user-function.js'
        with open(uf_filepath, "w") as uf_fd:
            uf_fd.write(uf)
            print 'Function loaded'

        return directory

    def run(self, fid, directory):

        print 'Start building docker...'
        image_name          = self.__build_docker(fid, directory)

        print 'Start running docker...'
        port, container_id  = self.__run_docker(image_name)

        print 'waiting for docker...'
        self.__wait_until_ready(port)

        return image_name, port, container_id

    def __build_docker(self, fid, directory):
        image_name = IMAGE_NAME_PREFIX + fid
        self.__exec(['docker', 'build', '-t', image_name, directory])
        return image_name

    def __run_docker(self, image_name):

        port = random.randint(1024 ,65535)  # random
        print 'Docker client listening on port: ' + str(port)

        run_cmd = ['docker', 'run', '-d', '-p', str(port) + ':8080', image_name]
        print run_cmd
        container_id = self.__exec(run_cmd)[:12]
        print 'Docker container id: ' + container_id
        return port, container_id

    def __wait_until_ready(self, port):

        while True:
            time.sleep(HEARTBEAT_PERIOD)
            url = 'http://localhost:' + str(port) + '/heartbeat'
            req = Request(url)
            print 'Heartbeat sent to ' + url
            try:
                response = urlopen(req)
            except:
                pass
            else:
                print 'Okay, function is up'
                break

    def stop(self, container_id, directory):
        self.__stop_docker(container_id)
        self.__remove_cache(directory)

    def __stop_docker(self, container_id):
        output = self.__exec(['docker', 'stop', container_id])
        print 'Docker container stopped ' + output

    def __remove_cache(self, directory):
        self.__exec(['rm', '-rf', directory])
        print 'Cache cleaned'

    def __exec(self, cmd):

        output = check_output(cmd)
        print output
        return output
