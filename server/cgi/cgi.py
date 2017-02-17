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

NODEJS_TEMPLATE             = './node-template'
DOCKER_IMAGE_NAME_PREFIX    = 'clofly/nodejs-user-function-'
SERVER_HEARTBEAT_PERIOD     = 0.01

MONGODB_SERVER              = 'ec2-54-92-149-222.compute-1.amazonaws.com'

start_time = time.time()

def main():

    print 'Content-Type: text/plain\n'

    # get function id
    fid = os.environ['PATH_INFO'][1:]

    # run in docker
    run_docker(fid)
    print('--- %s seconds ---' % (time.time() - start_time))


def run(cmd):

    output = check_output(cmd)
    print output
    return output


def load_user_function_code(uf_url, uf_local_zip, uf_local_folder, target_folder):

    # copy template folder to target folder
    run(['cp', '-r', NODEJS_TEMPLATE, target_folder])

    # download user code
    run(['wget', uf_url])

    # unzip
    run(['unzip', uf_local_zip, '-d', uf_local_folder])

    # load code
    run(['rsync', '-a', uf_local_folder, target_folder])

    # loaded
    print 'code loaded'

def run_docker(fid):

    # name/path setup
    docker_folder = NODEJS_TEMPLATE + '-' + fid
    docker_image_name = DOCKER_IMAGE_NAME_PREFIX + fid

    # user function code
    uf_url          = 'https://s3.amazonaws.com/clofly/uf-' + fid + '.zip'
    uf_local_zip    = 'uf-' + fid + '.zip'
    uf_local_folder = 'uf-' + fid + '/'

    # load user code
    load_user_function_code(uf_url, uf_local_zip, uf_local_folder,
                            docker_folder)
    print('--- %s seconds ---' % (time.time() - start_time))

    # build
    run(['docker', 'build', '-t', docker_image_name, docker_folder])
    print('--- %s seconds ---' % (time.time() - start_time))

    # remove unneed files
    run(['rm', '-r', uf_local_zip, uf_local_folder, docker_folder])

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
