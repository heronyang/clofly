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

NODEJS_TEMPLATE             = '../node-template'
DOCKER_IMAGE_NAME_PREFIX    = 'clofly/nodejs-user-function-'
SERVER_HEARTBEAT_PERIOD     = 0.01

MONGODB_SERVER              = 'ec2-54-92-149-222.compute-1.amazonaws.com'

start_time = time.time()

# Setting only for debug mode
if 'CLOFLY_DEBUG' in os.environ:
    NODEJS_TEMPLATE = './node-template'

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


def run(cmd):

    output = check_output(cmd)
    print output
    return output

def retrieve_user_function_code(fid):

    client = MongoClient(MONGODB_SERVER)
    db = client.clofly
    uf = db.userfunctions.find_one({'_id': ObjectId(fid)})['code']

    if not bool(uf):
        print 'Function not Found'
        sys.exit(0)

    print 'User Function: \n' + uf
    return uf

def load_user_function_code(uf, target_folder):

    # copy template folder to target folder
    run(['cp', '-r', NODEJS_TEMPLATE, target_folder])

    # load code
    uf_filepath = target_folder + '/user-function.js'
    with open(uf_filepath, "w") as uf_js:
        uf_js.write(uf)
        print 'code loaded'


def run_docker(user_function_code, fid):

    # name/path setup
    docker_folder = NODEJS_TEMPLATE + '-' + fid
    docker_image_name = DOCKER_IMAGE_NAME_PREFIX + fid

    # load user code
    load_user_function_code(user_function_code, docker_folder)
    print('--- %s seconds ---' % (time.time() - start_time))

    # build
    run(['docker', 'build', '-t', docker_image_name, docker_folder])
    print('--- %s seconds ---' % (time.time() - start_time))

    # run
    port = random.randint(1024 ,65535)  # random
    print 'docker client listening on port ' + str(port)

    run_cmd = ['docker', 'run', '-d', '-p', str(port) + ':8080', docker_image_name]
    container_id = run(run_cmd)[:12]
    print 'docker container id: ' + container_id
    print('--- %s seconds ---' % (time.time() - start_time))

    # block and wait for docker
    block_util_docker_is_up(port)
    print('--- %s seconds ---' % (time.time() - start_time))

    # forward request
    forward_request_to_docker(port)

    # stop docker image
    output = run(['docker', 'stop', container_id])
    print 'docker container stopped ' + output

    # remove docker_folder
    run(['rm', '-rf', docker_folder])

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

if __name__ == '__main__':
    main()
