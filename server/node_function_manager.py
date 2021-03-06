#!/usr/bin/env python

import sys, os
import random
import time
import httplib
import boto3
import psutil
import subprocess, signal
from shutil import copyfile
from subprocess import check_output
from urllib2 import Request, urlopen, URLError, HTTPError
from socket import error as SocketError
from function_manager_abstract import FunctionManagerAbstract

NODEJS_TEMPLATE     = './node-template'
IMAGE_NAME_PREFIX   = 'clofly/nodejs-user-function-'
HEARTBEAT_PERIOD    = 0.01

class FunctionManager(FunctionManagerAbstract):

    def __init__(self):
        os.environ['NODE_PATH'] = '/usr/local/lib/node_modules/'

    def __get_fid_dir(self, fid):
        escape_fid = fid.replace('/', '.')
        return NODEJS_TEMPLATE + '.' + escape_fid

    def load(self, fid):

        # load requested function to disk
        print 'Loading function id: ' + fid

        # downlaod from database
        uf = self.__download_function(fid)

		# setup working directory
        directory = self.__get_fid_dir(fid)
        return self.__setup_directory(directory, uf)

    def __download_function(self, fid):

        db          = boto3.resource('dynamodb')
        table       = db.Table('user-function')
        response    = table.get_item( Key={ 'fid': fid })
        uf          = response['Item']['code']

        if not bool(uf):
            raise Exception('Function not found')

        return uf

    def __setup_directory(self, directory, uf):

        # copy template folder to target folder
        self.__exec(['cp', '-r', NODEJS_TEMPLATE, directory])

        # load code
        uf_filepath = directory + '/user-function.js'
        with open(uf_filepath, "w") as uf_fd:
            uf_fd.write(uf)
            print 'Function loaded'

        return directory

    def run(self, fid, directory):

        print 'Start running node...'
        port, process = self.__run_node(directory)

        print 'Waiting for node...'
        self.__wait_until_ready(port)

        return port, process

    def __run_node(self, directory):

        port = random.randint(1024 ,65535)  # random

        cwd = os.getcwd()

        os.chdir(directory)
        process = subprocess.Popen(['./run.sh', str(port)]) # non-blocking
        os.chdir(cwd)

        return port, process

    def __wait_until_ready(self, port):

        url = 'http://localhost:' + str(port) + '/heartbeat'
        print 'Heartbeat start sending to ' + url

        while True:
            time.sleep(HEARTBEAT_PERIOD)
            req = Request(url)
            try:
                response = urlopen(req)
            except:
                pass
            else:
                print 'Okay, function is up'
                break

    def stop(self, process, directory):
        self.__kill_process(process)
        self.__remove_cache(directory)

    def __kill_process(self, process):

        p = psutil.Process(process.pid)
        for proc in p.children(recursive=True):
            print 'killing child process: ', p.pid
            proc.kill()
        print 'killing working process: ', process.pid
        p.kill()

    def __remove_cache(self, directory):
        self.__exec(['rm', '-rf', directory])
        print 'Cache cleaned'

    def __exec(self, cmd):

        output = check_output(cmd)
        print output
        return output
