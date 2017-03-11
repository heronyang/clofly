#!/usr/bin/env python

import boto3
from Crypto.Hash import SHA256
from flask import Flask, abort, request

# Flask app
app = Flask(__name__)

# DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('user')

@app.route("/login/", methods = ['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username == None or password == None:
        abort(400)  # Bad Request

    response = table.get_item(
        Key={
            'username': username
        }
    )
    if 'Item' in response:
        db_password = response['Item']['password']
        if hash(password) == db_password:
            return 'Login Succeed'

    abort(401)

def hash(s):
    h = SHA256.new()
    h.update(s)
    return h.hexdigest()

@app.route("/upload/")
def upload():
    return "Hello World!"

if __name__ == "__main__":
    app.run()

