#!/usr/bin/env python
import os
import boto3
from datetime import datetime
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

    response = table.get_item( Key={ 'username': username })
    if 'Item' in response:
        db_password = response['Item']['password']
        if hash(password) == db_password:
            session['username'] = username
            return 'Login Succeed'

    abort(401)

@app.route("/upload", methods = ['POST'])
def upload():

    if not 'username' in session:
        abort(401)

    # parse params
    params = request.get_json()
    if not 'fname' in params  or not 'code' in params:
        abort(400)

    username    = session['username']
    fid         = username + '/' + params['fname']
    code        = params['code']
    now         = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')

    ctime       = now
    version     = 1

    table = dynamodb.Table('user-function')

    # check if exists
    response = table.get_item( Key={ 'fid': fid })
    if 'Item' in response:
        item = response['Item']

        if item['code'] == code and item['stat'] == 'on':
            return 'No update is found, skip'

        if item['stat'] == 'on':
            version = item['version'] + 1

        ctime   = item['ctime']

    # if not, create new
    table.put_item(
        Item={
            'fid': fid,
            'code': code,
            'ctime': ctime,
            'mtime': now, 
            'version': version,
            'stat': 'on'
        }
    )

    return 'Deployed at ' + CLOFLY_SERVER_URL + fid + ' (version: ' + str(version) + ')'

@app.route("/turn-off", methods = ['POST'])
def turn_off():

    if not 'username' in session:
        abort(401)

    # parse params
    params = request.get_json()
    if not 'fname' in params:
        abort(400)

    username    = session['username']
    fid         = username + '/' + params['fname']

    table = dynamodb.Table('user-function')

    # check if not exist
    response = table.get_item( Key={ 'fid': fid })
    if not 'Item' in response:
        return 'Function not found'

    # if it's already of
    item = response['Item']
    if item['stat'] == 'off':
        return 'It\'s already off'


    # turn it off
    table.update_item(
        Key={ 'fid':fid },
        UpdateExpression='set stat = :s',
        ExpressionAttributeValues={ ':s': 'off', }
    )

    return 'Okay, it\'s off'

@app.route('/logout', methods = ['POST'])
def logout():
    session.pop('username', None)
    return 'Logout Succeed'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="80")
