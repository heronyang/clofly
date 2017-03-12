#!/usr/bin/env python
import boto3
from Crypto.Hash import SHA256
from flask import Flask, abort, request, session, escape
import os

# Flask app
app = Flask(__name__)

# DynamoDB
dynamodb = boto3.resource('dynamodb')
app.secret_key = os.environ.get('FLASK_SECRET_KEY')

@app.route("/login/", methods = ['POST'])
def login():

    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])    

    table = dynamodb.Table('user')

    params = request.get_json()
    
    print(params)
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

def hash(s):
    h = SHA256.new()
    # h.update(s)
    h.update(s.encode('utf-8'))
    return h.hexdigest()

@app.route("/upload/", methods = ['POST'])
def upload():

    table = dynamodb.Table('user-function')

    params = request.get_json()
    if not 'fid' in params  or not 'code' in params:
        abort(400)
    
    fid     = params['fid']
    code    = params['code']

    table.put_item(
        Item={
            'fid': fid,
            'code': code
        }
    )

    return 'Upload Succeed'

@app.route('/logout/')
def logout():
    session.pop('username', None)
    return 'Logout Succeed'


if __name__ == "__main__":
    app.run()
