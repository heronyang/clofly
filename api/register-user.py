#!/usr/bin/env python

import random
import string
import boto3
from helper import hash

PASSWORD_LEN = 16

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('user')

def generate_random_password():
    password = ''.join(random.SystemRandom().choice(string.ascii_uppercase \
        + string.ascii_lowercase +string.digits) for _ in range(PASSWORD_LEN))
    return password

def insert_to_database(username, password):

   password_hash = hash(password)
   table.put_item(
       Item = {
           'username': username,
           'password': password_hash
       }
   )

def main():

    username = raw_input('Username: ')
    password = generate_random_password()

    insert_to_database(username, password)
    print 'Done.'
    print 'Username: ' + username
    print 'Password: ' + password

if __name__ == "__main__":
    main()
