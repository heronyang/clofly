#!/usr/bin/env python
import sys, os, subprocess
import random
from pymongo import MongoClient
from bson.objectid import ObjectId
from pprint import pprint
from shutil import copyfile
from subprocess import check_output

NODEJS_TEMPLATE             = './node-template/'
NODEJS_TEMPLATE_ORIGINAL    = NODEJS_TEMPLATE + 'server-template.js'
NODEJS_TEMPLATE_DEPLOY      = NODEJS_TEMPLATE + 'server.js'

DOCKER_BUILD_SCRIPT         = './node-template/build.sh'
DOCKER_IMAGE_NAME_PREFIX    = 'darf/nodejs-user-function-'

def main():

    print 'Content-Type: text/plain\n'

    # get function id
    fid = os.environ['PATH_INFO'][1:]

    # retrieve function code
    uf = retrieve_user_function_code(fid)

    # run in docker
    run_docker(uf, fid)

    # clean up
    clean_up()

    # return
    return_http_response()

def retrieve_user_function_code(fid):

    client = MongoClient()
    db = client.dasf
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

	# run
    port = random.randint(1024 ,65535)  # random
    print 'docker client listening on port ' + str(port)

    run_cmd = ['docker', 'run', '-d', '-p', str(port) + ':8080', docker_image_name]
    output = check_output(run_cmd)
    print output


def clean_up():
    os.remove(NODEJS_TEMPLATE_DEPLOY)

def return_http_response():
    print 'Content-Type: text/plain\n'
    print 'Requested path: ' + os.environ['PATH_INFO']
    print '========= OS Environment Items =========\n'
    pprint(os.environ.items())

if __name__ == '__main__':
    main()
