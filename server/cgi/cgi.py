#!/usr/bin/env python

import sys, os, subprocess
import random
import time
import httplib
import cgi
import errno
from pymongo import MongoClient
from bson.objectid import ObjectId
from pprint import pprint
from shutil import copyfile
from subprocess import check_output
from urllib2 import Request, urlopen, URLError, HTTPError
from socket import error as SocketError

NODEJS_TEMPLATE             = './node-template/'
NODEJS_TEMPLATE_ORIGINAL    = NODEJS_TEMPLATE + 'server-template.js'
NODEJS_TEMPLATE_DEPLOY      = NODEJS_TEMPLATE + 'server.js'

DOCKER_IMAGE_NAME_PREFIX    = 'clofly/nodejs-user-function-'

SERVER_HEARTBEAT_PERIOD     = 0.01

start_time = time.time()

def main():

    print 'Content-Type: text/plain\n'

    # get function id
    fid = os.environ['PATH_INFO'][1:]

    # retrieve function code
    uf = retrieve_user_function_code(fid)

    print('--- %s seconds ---' % (time.time() - start_time))

    # run in docker
    run_docker(uf, fid)

    print('--- %s seconds ---' % (time.time() - start_time))

    # clean up
    clean_up()

    print('--- %s seconds ---' % (time.time() - start_time))

def retrieve_user_function_code(fid):

    client = MongoClient()
    db = client.clofly
    uf = db.userfunctions.find_one({'_id': ObjectId(fid)})['code']

    print 'User Function: \n' + uf
    return uf

def append_user_function_code(uf):

    # copy
    copyfile(NODEJS_TEMPLATE_ORIGINAL, NODEJS_TEMPLATE_DEPLOY)

    # code to append
    code = "\napp.get('/', " + uf + ");"

    # append code
    with open(NODEJS_TEMPLATE_DEPLOY, "a") as serverjs:
        serverjs.write(code)
        print 'code appended'


def run_docker(user_function_code, fid):

    append_user_function_code(user_function_code)
    docker_image_name = DOCKER_IMAGE_NAME_PREFIX + fid

    # build
    build_cmd = ['docker', 'build', '-t', docker_image_name, NODEJS_TEMPLATE]
    output = check_output(build_cmd)
    print output

    print('--- %s seconds ---' % (time.time() - start_time))

    # run
    port = random.randint(1024 ,65535)  # random
    print 'docker client listening on port ' + str(port)

    run_cmd = ['docker', 'run', '-d', '-p', str(port) + ':8080', docker_image_name]
    container_id = check_output(run_cmd)[:12]
    print 'docker container id: ' + container_id
    # TODO: use docker API solution
    # client = docker.from_env()
    # ports = {str(port):'8080'}
    # container = client.containers.run(docker_image_name, ports=ports, detach=True)

    print('--- %s seconds ---' % (time.time() - start_time))

    # block and wait for docker
    block_util_docker_is_up(port)

    print('--- %s seconds ---' % (time.time() - start_time))

    # forward request
    forward_request_to_docker(port)

    # stop docker image
    stop_cmd = ['docker', 'stop', container_id]
    output = check_output(stop_cmd)
    print 'docker container stopped ' + output

    # TODO: use docker API solution
    # container.stop()

def block_util_docker_is_up(port):

    # list on port (server)
    while True:
        time.sleep(SERVER_HEARTBEAT_PERIOD)
        url = 'http://localhost:' + str(port) + '/heartbeat'
        req = Request(url)
        print 'heartbeat sent to ' + url
        try:
            response = urlopen(req)
        except HTTPError as e:
            pass
        except URLError as e:
            pass
        except httplib.BadStatusLine:
            pass
        except SocketError as e:
            pass
        else:
            print 'okay, function is up'
            break

def forward_request_to_docker(port):

    # TODO: should pack os.environ.items into the request
    url = 'http://localhost:' + str(port) + '/'
    req = Request(url)
    try:
        response = urlopen(req)
    except HTTPError as e:
        pass
    except URLError as e:
        pass
    except httplib.BadStatusLine:
        pass
    except SocketError as e:
        pass
    else:
        print "\n========= Response ============="
        print response.read()
        print "\n========= Response End ========="

def clean_up():
    os.remove(NODEJS_TEMPLATE_DEPLOY)

if __name__ == '__main__':
    main()
