#!/usr/bin/env python
import os
import boto3
from flask import Flask, abort, request, session, escape
from helper import hash

CLOFLY_SERVER_URL = 'http://clofly.com/'

# Flask app
app = Flask(__name__)
app.url_map.strict_slashes = False
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default_flask_key')

# DynamoDB
dynamodb = boto3.resource('dynamodb')

@app.route("/login", methods = ['POST'])
def login():

    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])    

    table = dynamodb.Table('user')
    params = request.get_json()
    
    if not 'username' in params  or not 'password' in params:
        abort(400)

    username = params['username']
    password = params['password']

    response = table.get_item(
        Key={
            'username': username
        }
    )
    if 'Item' in response:
        db_password = response['Item']['password']
        if hash(password) == db_password:
            session['username'] = username
            return 'Login Succeed'

    abort(401)

@app.route("/upload", methods = ['POST'])
def upload():

    # if not logged in
    if not 'username' in session:
        abort(401)

    # parse params
    params = request.get_json()
    if not 'fname' in params  or not 'code' in params:
        abort(400)

    # get version and increase version
    
    username    = session['username']
    fid         = username + '/' + params['fname']
    code        = params['code']
    version     = str(insert_new_version(fid))

    table = dynamodb.Table('user-function')

    # store latest at /fid
    table.put_item( Item={ 'fid': fid, 'code': code })
    # store at /fid/version
    table.put_item( Item={ 'fid': fid + '/' + version, 'code': code })

    return 'Deployed at ' + CLOFLY_SERVER_URL + fid

def insert_new_version(fid):

    # get latest version
    latest_version = 0
    table = dynamodb.Table('user-function-version')
    response = table.get_item( Key={ 'fid': fid })
    if 'Item' in response:
        latest_version = response['Item']['version']

    # insert new version
    new_version = latest_version + 1
    table.put_item( Item={ 'fid': fid, 'version': new_version } )

    return new_version

@app.route('/logout')
def logout():
    session.pop('username', None)
    return 'Logout Succeed'

if __name__ == "__main__":
    app.run()
