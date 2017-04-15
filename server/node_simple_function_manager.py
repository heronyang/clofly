#!/usr/bin/env python

import sys, os
import random
import time
import boto3
import psutil
import subprocess
from urllib2 import Request, urlopen
from function_manager_abstract import FunctionManagerAbstract

HEARTBEAT_PERIOD = 0.01
CACHE_FOLDER     = './cached-user-function/'

class FunctionManager(FunctionManagerAbstract):

    def __init__(self):
        os.environ['NODE_PATH'] = '/usr/lib/node_modules'

    def __get_cached_uf_filename(self, fid):
        escape_fid = fid.replace('/', '.')
        return CACHE_FOLDER + escape_fid + '.js'

    def load(self, fid):

        # load requested function to disk
        print 'Loading function id: ' + fid

        # downlaod from database
        uf = self.__download_function(fid)

        return uf

		# save to disk
        # return self.__save_to_disk(fid, uf)

    def __download_function(self, fid):

        db          = boto3.resource('dynamodb')
        table       = db.Table('user-function')
        response    = table.get_item( Key={ 'fid': fid })
        uf          = response['Item']['code']

        if not bool(uf):
            raise Exception('Function not found')

        return uf

    def __save_to_disk(self, fid, uf):

        # load code
        uf_filepath = self.__get_cached_uf_filename(fid)
        with open(uf_filepath, "w") as uf_fd:
            uf_fd.write(uf)
            print 'Function loaded'

        return None

    def run(self, fid, uf):

        print 'Start running node...'
        port, process = self.__run_node(fid)

        print 'Waiting for node...'
        self.__wait_until_ready(port)

        return port, process

    def __run_node(self, uf):

        port = random.randint(1024 ,65535)  # random
        process = subprocess.Popen(['./starter.js', str(port), uf]) # non-blocking

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

    def __kill_process(self, process):

        p = psutil.Process(process.pid)
        for proc in p.children(recursive=True):
            print 'killing child process: ', p.pid
            proc.kill()
        print 'killing working process: ', process.pid
        p.kill()
